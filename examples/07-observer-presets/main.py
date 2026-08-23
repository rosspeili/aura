"""Example 07 — Monitor and Break observer presets on a ToolHost session."""

from __future__ import annotations

import json

from aura import agent, configure
from aura.hosts import MockSkill, SkillwareHost


def main() -> None:
    configure()
    ag = agent(
        "observer-presets-demo",
        purpose="After-call analytics and circuit-breaker alerts on the audit spine",
        observers=[
            {"preset": "monitor", "id": "loop-monitor", "config": {"max_identical_intents": 2}},
            {"preset": "break", "id": "loop-break", "config": {"max_identical_intents": 3}},
        ],
    )

    with ag.session(mode="script") as run:
        host = SkillwareHost(run._session)
        host.register(MockSkill("ops", {"ping": lambda a: {"ok": True}}))
        for _ in range(4):
            host.execute("ops", "ping", {"n": 1})
        run.emit("turn.end", {"output": "observer preset demo complete"})

    kinds = [e.kind for e in run._session.spine.stream()]
    print(
        json.dumps(
            {
                "session_id": run.session_id,
                "observer_notes": kinds.count("observer.note"),
                "observer_alerts": kinds.count("observer.alert"),
                "tool_calls": kinds.count("tool.call"),
            },
            indent=2,
        )
    )
    print("exports:", run.exports)


if __name__ == "__main__":
    main()
