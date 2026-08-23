# Anthropic (Claude) + Skillware + AURA

Run Claude as the **body** and Skillware skills at AURA **egress**.

## Where AURA sits

```
┌─────────────┐     ┌──────────────┐     ┌─────────────────┐
│  Anthropic  │     │  Your script │     │    Skillware    │
│  (body LLM) │◄────│  + AURA      │────►│  (tool skills)  │
└─────────────┘     │  session     │     └─────────────────┘
                    │  audit spine │
                    └──────────────┘
```

| Layer | Owns |
|---|---|
| **Anthropic API** | Claude messages, system prompts |
| **Skillware** | Skill bundles, offline/online tools |
| **AURA** | Audit spine, egress constraints, session export |
| **Your script** | Orchestration — model turn vs skill calls |

Claude handles language; Skillware handles deterministic tools; AURA proves the tool boundary was enforced.

## When to add AURA

Use AURA on top of Skillware + Claude when:

- Tool calls must be **allowlisted** or **human-approved** (e.g. `office/gmail_handler`)
- You need a **hash-chained audit report** for regulators or internal security
- You run **fixed pipelines** (sequencer) and must prove step order

## Setup

```powershell
.venv\Scripts\activate
pip install -e ".[skillware,anthropic]"
copy .env.example .env
```

```
ANTHROPIC_API_KEY=sk-ant-...
ANTHROPIC_MODEL=claude-sonnet-4-20250514
```

## Run

```powershell
python integrations/anthropic/skillware_body_loop.py
```

Flow: AURA session → Claude narration → Skillware firewall at egress → session export.

## Best practices

1. **Scan before context** — run `security/prompt_injection_firewall` on untrusted input before inserting into Claude messages
2. **Emit model calls** — `run.emit("model.call", {...})` so spine shows body vs tool separation
3. **Manifest guardrails** — add `guardrails.deny_tools` on skills that send email or move funds

## Related

- [Full Skillware + AURA guide](../../docs/guides/aura-on-skillware.md)
- [OpenAI integration](../openai/README.md)
- [Gemini integration](../google/README.md)
