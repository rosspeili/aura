# Skillware integration (reference adapter)

AURA wraps [Skillware](https://github.com/arpahls/skillware) at **egress** — policy, approval, and audit on every tool call. Skillware supplies installable skills; AURA does not replace Skillware's runtime.

## Install

```bash
pip install -e ".[dev,skillware]"   # aura-harness + skillware>=0.5.1
pip install ollama                  # optional — Ollama body loop only
```

Copy [`.env.example`](../../.env.example) to `.env` for `OLLAMA_MODEL=llama3.2:1b` and local Ollama URL.

Optional full dev stack: `pip install -e ".[dev,integrations]"` (adds `ollama` client).

Verify Skillware:

```bash
skillware list
skillware doctor optimization/prompt_rewriter
skillware doctor security/prompt_injection_firewall
```

## Scripts

| Script | Purpose |
|---|---|
| [`reference_tool_host.py`](reference_tool_host.py) | Mock (default) or live Skillware via `SKILLWARE_LIVE=1` |
| [`ollama_skill_loop.py`](ollama_skill_loop.py) | Ollama `llama3.2:1b` + real `prompt_injection_firewall` through AURA |

### Mock (CI-safe, no Skillware registry)

```bash
python integrations/skillware/reference_tool_host.py
```

### Live Skillware registry skills

Uses bundled offline skills from the installed `skillware` package:

```bash
# PowerShell
$env:SKILLWARE_LIVE = "1"
python integrations/skillware/reference_tool_host.py
```

Recommended starter skills (no API keys, offline):

- `optimization/prompt_rewriter` — token compression
- `security/prompt_injection_firewall` — pre-LLM injection scan
- `monitoring/token_limiter` — budget gate

### Ollama + Skillware under AURA

```bash
ollama pull llama3.2:1b
ollama serve   # if not already running
python integrations/skillware/ollama_skill_loop.py
```

## Python API

```python
from aura import agent, configure
from aura.hosts import SkillwareHost, load_registry_skill

configure()
with agent("demo", skills=["security/prompt_injection_firewall"]).session() as run:
    host = SkillwareHost(run._session)
    host.register_registry_skill("security/prompt_injection_firewall")
    result = host.execute(
        "security/prompt_injection_firewall",
        "security/prompt_injection_firewall",
        {"source_text": untrusted_text, "sensitivity": "balanced"},
    )
```

Or load explicitly:

```python
skill = load_registry_skill("optimization/prompt_rewriter")
host.register(skill)
host.execute(skill.skill_id, skill.skill_id, {"raw_text": "...", "compression_aggression": "medium"})
```

## Skillware vs AURA manifest fields

| Skillware manifest | AURA at bind |
|---|---|
| `name`, `parameters`, `constitution` | Recorded in `skill.registered` snapshot hash |
| Optional `guardrails:` block (AURA extension) | Merged into session constraint rules |
| `constitution` (text) | Audit metadata only — not auto-enforced as machine rules |

Add a `guardrails` key to a skill manifest overlay when you need allow/deny/confirm rules at bind time.

## Architecture

```
Session open → membrane.ingress
Skill register → skill.registered (+ optional rule merge)
Tool call → tool.intent → tool.call (constraints) → Skillware.execute(params) → tool.result
Session close → JSONL + summary + audit report
```

Parent epic: [#12](https://github.com/ARPAHLS/aura/issues/12) · Loader: `aura.hosts.load_registry_skill` · Host: `aura.hosts.SkillwareHost`

Full guide: [`docs/skillware-integration.md`](../../docs/skillware-integration.md)
