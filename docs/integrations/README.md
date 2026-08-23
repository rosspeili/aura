# Integrations

Attach AURA to your stack — models, tool runtimes, frameworks, sandboxes.

**Skillware + AURA:** start with [guides/aura-on-skillware.md](../guides/aura-on-skillware.md).

| Integration | Path | Notes |
|---|---|---|
| **Overview** | this page | Start here to find your stack |
| **Skillware** | [`integrations/skillware/`](../../integrations/skillware/) | Reference ToolHost adapter; `[skillware]` extra |
| **Ollama (local)** | [`integrations/skillware/ollama_skill_loop.py`](../../integrations/skillware/ollama_skill_loop.py) | Dev default: `llama3.2:1b` via `.env` |
| **OpenAI (ChatGPT)** | [`integrations/openai/`](../../integrations/openai/) | Body loop + Skillware egress; `[openai]` extra |
| **Anthropic (Claude)** | [`integrations/anthropic/`](../../integrations/anthropic/) | Body loop + Skillware egress; `[anthropic]` extra |
| **Google Gemini** | [`integrations/google/`](../../integrations/google/) | Body loop + Skillware egress; `[google]` extra |
| **LangGraph / CrewAI** | planned | Framework wrap examples |

Copy [`.env.example`](../../.env.example) to `.env` for local Ollama or cloud API keys. Do not commit `.env`.

Use the project **`.venv`** for installs (`pip install -e ".[integrations]"`), not global Python.

## Runnable examples

| Example | Shows |
|---|---|
| [05-skillware-skill-types](../examples/05-skillware-skill-types/) | Three skill categories under AURA |
| [06-skillware-sequencer-chain](../examples/06-skillware-sequencer-chain/) | Sequencer skill chain |
| [04-sequencer-pipeline](../examples/04-sequencer-pipeline/) | Sequencer with mocks |

## Related docs

- [skillware-integration.md](../skillware-integration.md) — API reference
- [sequencer.md](../sequencer.md) — step model and gates
- [skillware-follow-ups.md](../guides/skillware-follow-ups.md) — post-merge issue backlog
