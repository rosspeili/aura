# Example 05 — Skillware skill types under AURA

Demonstrates **three different Skillware categories** in one audited session:

| Step | Skill | Category | What it shows |
|---|---|---|---|
| Scan | `security/prompt_injection_firewall` | Security | Pre-LLM injection scan (offline) |
| Compress | `optimization/prompt_rewriter` | Optimization | Token compression |
| Budget | `monitoring/token_limiter` | Monitoring | Deterministic budget gate |

Each call passes through **AURA egress** — you get `tool.intent`, `tool.call`, `tool.result`, and optional `skill.registered` on the spine.

## Run (mock — CI-safe, no Skillware install)

From repo root with the project venv:

```powershell
.venv\Scripts\activate
pip install -e ".[dev]"
python examples/05-skillware-skill-types/main.py
```

## Run (live Skillware registry skills)

```powershell
pip install -e ".[skillware]"
$env:SKILLWARE_LIVE = "1"
python examples/05-skillware-skill-types/main.py
```

Verify skills: `skillware doctor security/prompt_injection_firewall`

## Why AURA here?

Skillware runs the skill logic. AURA records **who** invoked **which** skill, enforces constitution rules at egress, and exports a session you can audit or fail in CI via `conformance.passed`.

→ Full guide: [docs/guides/aura-on-skillware.md](../../docs/guides/aura-on-skillware.md)
