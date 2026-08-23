"""Tests for sequencer, observers, and Skillware host."""

from __future__ import annotations

import pytest

from aura import agent, ApprovalRequired
from aura.core.constraints import ConstraintViolation
from aura.core.conformance import ConformanceEngine
from aura.hosts.mock import MockSkill
from aura.hosts.skillware import SkillwareHost
from aura.observers.base import CallableObserver, get_registry
from aura.sequencer import load_steps

PIPELINE = {
    "steps": [
        {
            "id": "research",
            "type": "skill",
            "ref": "research",
            "config": {"tool": "search", "args": {"q": "aura"}},
        },
        {"id": "draft", "type": "op", "ref": "compose"},
        {
            "id": "send",
            "type": "skill",
            "ref": "gmail",
            "gates": ["human_confirm"],
            "config": {"tool": "send", "args": {"to": "team@example.com"}},
        },
    ]
}


def test_sequencer_linear_steps(aura_home):
    spec = {
        "steps": [
            {
                "id": "research",
                "type": "skill",
                "ref": "research",
                "config": {"tool": "search", "args": {"q": "aura"}},
            },
            {"id": "draft", "type": "op", "ref": "compose"},
        ]
    }
    ag = agent("seq-linear", sequencer=spec)
    with ag.session(export=False) as run:
        skill = MockSkill("research", {"search": lambda a: {"hits": 1}})
        host = SkillwareHost(run._session)
        host.register(skill)
        result = run.run_sequencer(host=host)
    assert result["completed"] == ["research", "draft"]


def test_sequencer_human_confirm_gate(aura_home):
    ag = agent("seq-gate", sequencer=PIPELINE)
    with ag.session(export=False) as run:
        host = SkillwareHost(run._session)
        host.register(MockSkill("research", {"search": lambda a: {}}))
        host.register(MockSkill("gmail", {"send": lambda a: {"sent": True}}))
        with pytest.raises(ApprovalRequired) as exc:
            run.run_sequencer(host=host)
        run.approve(exc.value.request_id)
        result = run.run_sequencer(host=host)
    assert "send" in result["completed"]


def test_observer_receives_events(aura_home):
    seen: list[str] = []
    reg = get_registry()
    reg.register(CallableObserver("test-obs", lambda e: seen.append(e["kind"])))
    ag = agent("obs-test")
    with ag.session(export=False) as run:
        run.emit("turn.start", {})
    assert "turn.start" in seen
    reg.unregister("test-obs")


def test_membrane_ingress_on_open(aura_home):
    ag = agent("ingress-test", skills=["research"])
    with ag.session(export=False) as run:
        pass
    events = run._session.spine.stream()
    assert any(e.kind == "membrane.ingress" for e in events)


def test_egress_tool_audit(aura_home):
    ag = agent("egress-test")
    with ag.session(export=False) as run:
        host = SkillwareHost(run._session)
        host.register(MockSkill("demo", {"ping": lambda a: "pong"}))
        host.execute("demo", "ping", {})
    kinds = [e.kind for e in run._session.spine.stream()]
    assert "tool.intent" in kinds
    assert "tool.call" in kinds
    assert "tool.result" in kinds


def test_conformance_sequencer_order(aura_home):
    ag = agent("conf-seq", sequencer={"steps": [{"id": "a", "type": "op", "ref": "x"}]})
    with ag.session(export=False) as run:
        run.run_sequencer()
    report = ConformanceEngine().summarize(
        run._session.spine,
        run._session.rules,
        run._session.snapshot_hash,
        sequencer_spec=ag.profile.sequencer,
    )
    assert report.passed is True
    assert any(c.get("type") == "sequencer" for c in report.checks)


def test_load_steps():
    steps = load_steps(PIPELINE)
    assert len(steps) == 3
    assert steps[0].step_type == "skill"


def test_skill_manifest_merge_blocks_denied_tool(aura_home):
    ag = agent("manifest-deny")
    manifest = {"deny_tools": ["delete.db"]}
    with ag.session(export=False) as run:
        host = SkillwareHost(run._session)
        host.register(
            MockSkill("ops", {"delete.db": lambda a: {"deleted": True}}, manifest=manifest)
        )
        with pytest.raises(ConstraintViolation):
            host.execute("ops", "delete.db", {})
    kinds = [e.kind for e in run._session.spine.stream()]
    assert "skill.registered" in kinds
    assert "constraint.violated" in kinds


def test_skill_registered_ingress_payload(aura_home):
    ag = agent("manifest-bind", agent_ref="acme/bind-test")
    manifest = {"allow_tools": ["search"]}
    with ag.session(export=False) as run:
        host = SkillwareHost(run._session)
        host.register(MockSkill("research", {"search": lambda a: {}}, manifest=manifest))
    registered = [e for e in run._session.spine.stream() if e.kind == "skill.registered"]
    assert len(registered) == 1
    payload = registered[0].payload
    assert payload["skill_id"] == "research"
    assert payload["agent_ref"] == "acme/bind-test"
    assert payload["manifest_snapshot_hash"]


def test_monitor_observer_preset(aura_home):
    ag = agent(
        "monitor-preset",
        observers=[{"preset": "monitor", "id": "loop-monitor", "config": {}}],
    )
    with ag.session(export=False) as run:
        host = SkillwareHost(run._session)
        host.register(MockSkill("demo", {"ping": lambda a: "pong"}))
        host.execute("demo", "ping", {})
        host.execute("demo", "ping", {})
    kinds = [e.kind for e in run._session.spine.stream()]
    assert "observer.note" not in kinds  # no repeat threshold by default
    assert "tool.call" in kinds
