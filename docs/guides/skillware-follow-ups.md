# Skillware + AURA — follow-up issues (suggested)

Track these **after** merging the reference-host / Skillware integration PR. They extend docs, CI, and capstone demos without blocking the core adapter.

---

## CI & quality

| Title | Scope |
|---|---|
| **CI Skillware matrix job** ([#36](https://github.com/ARPAHLS/aura/issues/36)) | Install `[skillware]` on runner; run `pytest -m skillware`; optional weekly live job |
| **Integration script smoke in CI** | Run `reference_tool_host.py` mock path; `examples/05`, `06` without `SKILLWARE_LIVE` |
| **Provider integration opt-in job** | Manual `workflow_dispatch` with secrets for OpenAI/Anthropic/Gemini smoke |

---

## Documentation & examples

| Title | Scope |
|---|---|
| **Flat examples restructure** ([#41](https://github.com/ARPAHLS/aura/issues/41)) | Align paths referenced in docs after examples move |
| **Capstone: multi-provider comparison** ([#40](https://github.com/ARPAHLS/aura/issues/40)) | One doc page comparing Ollama vs GPT vs Claude vs Gemini with same Skillware chain |
| **Skill catalog appendix** | Table of bundled Skillware skills: offline vs API, suggested AURA guardrails |
| **Video / walkthrough** | 5-minute demo: mock → live → sequencer → export |

---

## Product / adapter

| Title | Scope |
|---|---|
| **Constitution → rules mapper** | Optional transform of Skillware constitution text to AURA machine rules (opt-in) |
| **Break observer preset** ([#34](https://github.com/ARPAHLS/aura/issues/34)) | Loop detection on repeated tool intents |
| **OTel principal enrichment** ([#35](https://github.com/ARPAHLS/aura/issues/35)) | Skillware skill id + manifest hash on spans |
| **`SkillwareHost` async execute** | If Skillware adds async skills, mirror at egress |

---

## Skillware-specific demos (nice-to-have)

| Skill | Demo idea |
|---|---|
| `compliance/pii_masker` | Pre-LLM redaction pipeline with Ollama micro-f1-mask |
| `office/gmail_handler` | Sequencer with `human_confirm` on send |
| `compliance/tos_evaluator` | Legal review chain with export for audit |

Each should follow the same pattern: **body LLM optional**, **skills at egress**, **AURA session export**.

---

## How to use this doc

Copy rows into GitHub issues when ready. Link back to [aura-on-skillware.md](aura-on-skillware.md) as the canonical integration guide.
