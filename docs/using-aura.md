# Using AURA Harness

How to attach AURA to **your** agent loop — whatever shape it takes. AURA is a runtime **membrane** (audit, policy, identity, export) around the body that runs inference and tools. It does not prescribe a product category, team size, or stack.

---

## Example usage patterns (illustrative)

The table below is **not** a product taxonomy or a checklist of “supported modes.” It shows three **common ways** teams describe their setup when adopting AURA. Mix, skip, or ignore them — use only the pieces you need (`emit()` only, full sequencer + Skillware, registry + batch compare, etc.).

| Pattern (example) | What people often want | One way to wire it |
|---|---|---|
| **Minimal wrap** | Record a custom loop; export for analysis | `agent().session()`, `emit()`, rules optional |
| **Prescriptive pipeline** | Declared steps, gates, CI conformance | Sequencer spec, `SkillwareHost`, session export in CI |
| **Multi-agent ops** | Many agents, compare runs programmatically | Registry + batch sessions + JSONL export / `aura compare` |

These rows come from real adoptions (including ARPA-internal batch flows) but **do not define** what AURA is for. The core contract is the same everywhere: open a session, run your body, append spine events, export on close.

AURA is the **harness (coat)**, not the runtime. Your **body** owns the loop; AURA wraps it with **membrane** boundaries and an **audit trail**.

---

## Membrane model

```
Ingress → [ Body / host cavity ] → Egress → Audit sink
              ↑
         Observers (parallel subscribers)
```

| Boundary | Role |
|---|---|
| **Ingress** | Normalize agent context at session open (`membrane.ingress` event) |
| **Body** | Your loop — script, Skillware host, LangGraph, device |
| **Egress** | Policy + audit before tools/skills execute (`tool.intent` → `tool.call` → `tool.result`) |
| **Observers** | Parallel handlers on every spine event — monitoring, alerts, custom analytics |
| **Audit sink** | Append-only JSONL + session export on close |

Ingress and egress are **conceptual boundaries** implemented in `aura/membrane/`. Observers never block the host.

---

## Python SDK (primary)

```python
from aura import agent, configure
from aura.hosts import SkillwareHost, MockSkill

configure()

ag = agent(
    "pipeline-bot",
    skills=["research", "gmail"],
    sequencer={"steps": [...]},
    rules=[{"type": "confirm_before", "tools": ["send"]}],
)

with ag.session(mode="task") as run:
    host = SkillwareHost(run._session)
    host.register(MockSkill("research", {"search": lambda a: {"hits": 1}}))
    run.run_sequencer(host=host)
```

| API | Purpose |
|---|---|
| `configure()` | Merge global + project config |
| `agent(name)` | Get/create agent profile |
| `agent.session()` | Open session, auto-export on close |
| `run.emit(kind, payload)` | Append audited event |
| `run.approve(request_id)` | Satisfy confirm/gate |
| `run.run_sequencer(host=...)` | Run declared step pipeline |
| `current_session()` | Active handle inside context |

Submodules: `aura.sequencer`, `aura.hosts`, `aura.observers`, `aura.membrane`.

---

## Sequencer vs emergent tool loop

| | **Sequencer** | **Emergent agent loop** |
|---|---|---|
| Control | You declare step order upfront | Model chooses tools step-by-step |
| Conformance | Declared steps vs spine on close | Rule checks per event only |
| Use case | Compliance pipelines, SOPs | Open-ended research, chat |

Both can coexist: run a sequencer inside a session, or emit events manually in a free-form loop.

Step types: `skill`, `op`, `prompt`, `gate`, `subflow`. Gates: `human_confirm`, `constitution`, `budget`.

→ [sequencer.md](sequencer.md) · [skillware-integration.md](skillware-integration.md)

---

## Observers

Register global or per-session subscribers:

```python
from aura.observers import CallableObserver, get_registry

get_registry().register(CallableObserver("metrics", lambda e: print(e["kind"])))
```

Profile observers (by id) attach at session open. Handlers must be non-blocking.

---

## CLI

Mirrors the SDK for agent management and script runs:

```bash
aura                    # interactive splash + menu (after pip install)
aura --help             # grouped command reference
aura config show        # merged config + resolved paths
aura paths              # view paths; set-project / set-storage persist YAML
aura agent create my-bot --purpose "compliance"
aura agent set my-bot --ref acme/my-bot --skill research --variable model=llama3.2
aura run my-bot examples/04-sequencer-pipeline/main.py
aura logs aura_sess_xxxxxxxxxxxx
aura export aura_sess_xxxxxxxxxxxx
```

Profiles live as JSON under `{AURA_HOME}/agents/`. Global defaults: `~/.aura/config.yaml`. Project overrides: `{project}/aura.project.yaml`. Use env vars for API keys; store non-secret refs in profile `variables`.

Interactive menu: **agents** (list/show/create/edit), **sessions**, **run**, **paths**, help, version.

---

## YAML agent profiles

Agent fields (JSON on disk under `~/.aura/agents/`):

```yaml
name: compliance-bot
purpose: Research → draft → approve → notify
skills: [research, gmail]
sequencer:
  steps:
    - id: research
      type: skill
      ref: research
      config: { tool: search, args: { query: "..." } }
    - id: notify
      type: skill
      ref: gmail
      gates: [human_confirm]
      config: { tool: send, args: { to: "team@example.com" } }
rules:
  - type: confirm_before
    tools: [send]
observers:
  - id: slack-alerts
```

Schema: [sequencer.schema.json](../spec/sequencer.schema.json)

---

## Optional Skillware

```bash
pip install "aura-harness[skillware]"
```

Skillware ≥ 0.5.1 runs inside the body; AURA wraps `execute()` at egress. See [skillware-integration.md](skillware-integration.md).

---

## What AURA does not own

- Model inference or tool implementation (body / Skillware)
- Full batch eval (RAGAS) — export feeds eval pipelines later
- HTTP fleet API — deferred

→ [comparison.md](comparison.md) · [ROADMAP.md](ROADMAP.md)
