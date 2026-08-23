# Skillware integration

AURA Harness wraps Skillware skills at **egress** — policy, approval, and audit — without owning Skillware's runtime.

---

## Position in the stack

| Layer | Owner |
|---|---|
| **Skillware** | Skill bundles, `execute()`, tool implementations |
| **Body / host** | Loads skills, runs the loop |
| **AURA membrane** | Ingress context, egress guard on every tool call |
| **Audit trail** | JSONL spine + session export |

Skillware is **optional**: `pip install "aura-harness[skillware]"` (requires Skillware ≥ 0.5.1). Tests and examples use `MockSkill` when Skillware is not installed.

---

## Quick start (mock skills)

Same host API as real Skillware — swap mocks for live skills later.

```python
from aura import agent, configure, ApprovalRequired
from aura.hosts import SkillwareHost, MockSkill

configure()

ag = agent("demo", skills=["research"])

with ag.session() as run:
    host = SkillwareHost(run._session)
    host.register(
        MockSkill("research", {"search": lambda args: {"results": []}})
    )
    host.execute("research", "search", {"query": "AURA harness"})
```

Every execution emits:

1. `skill.registered` — when the skill carries a manifest (merged into session rules)
2. `tool.intent` — egress intent
3. `tool.call` — constraint checks (allow/deny, confirm_before, …)
4. `tool.result` or `tool.error`

### Manifest guardrails at bind

Pass optional `manifest` on `MockSkill` (or on live skills) to merge allow/deny/confirm rules into the session constitution at register time:

```python
MockSkill(
    "gmail",
    {"send": lambda args: {"sent": True}},
    manifest={"deny_tools": ["send.bulk"]},
)
```

Emits `skill.registered` on the spine with `manifest_snapshot_hash`, `agent_ref`, and `policy_version`.

### Monitor observer preset

Add to agent profile `observers`:

```yaml
observers:
  - preset: monitor
    id: loop-monitor
    config:
      max_identical_intents: 5
      log_path: .aura/monitor.log
```

Tracks tool calls and emits `observer.note` events (analytics only — does not block egress).

---

## ToolHost protocol

Any runtime can implement `ToolHost` (`register`, `execute` through egress). `SkillwareHost` is the reference adapter — see `aura.hosts.ToolHost`.

---

## Real Skillware skills

```python
from aura.hosts import SkillwareHost, skillware_available

if skillware_available():
    # import your Skillware skill instances
    host = SkillwareHost.from_skillware(run._session, [research_skill, gmail_skill])
    run.run_sequencer(host=host)
```

`SkillwareHost.register_by_id()` wraps any object with `execute(tool, **args)` or `run(tool, **args)`.

---

## Constitution merge

Rules come from:

1. Agent profile `rules` (AURA constitution)
2. Session overrides passed to `agent.session(rules=[...])`
3. Future: skill manifest rules merged at bind time (roadmap)

Constraints apply at **egress** on `tool.call` — the same path as manual `emit("tool.call", ...)`.

---

## Sequencer + Skillware pipeline

Declare skills in sequencer steps; host routes `type: skill` steps through egress:

```yaml
sequencer:
  steps:
    - id: research
      type: skill
      ref: research
      config:
        tool: search
        args: { query: "compliance brief" }
    - id: send
      type: skill
      ref: gmail
      gates: [human_confirm]
      config:
        tool: send
        args: { to: "team@example.com", subject: "Brief" }
```

Runnable example: [examples/04-sequencer-pipeline](../examples/04-sequencer-pipeline/).

---

## CLI and CI

Run the example under an agent session:

```bash
pip install -e ".[dev]"
python examples/04-sequencer-pipeline/main.py
```

Use session export `.summary.json` `conformance.passed` in CI to fail builds when rules or sequencer order diverge.

---

## Related

- [using-aura.md](using-aura.md) — membrane and personas
- [sequencer.md](sequencer.md) — step model and gates
- [Skillware repo](https://github.com/arpahls/skillware)
