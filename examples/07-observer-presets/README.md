# Example 07 — Observer presets (Monitor + Break)

Shows **after-call** membrane analytics — observers subscribe to the spine and emit side signals. They **do not block** egress; enforcement stays at `tool.call`.

| Preset | Emits | Use |
|---|---|---|
| **monitor** | `observer.note` | Counts, timing, soft repeat warnings |
| **break** | `observer.alert` | Circuit-breaker when identical tool intents exceed threshold |

Uses `MockSkill` — any `ToolHost` adapter produces the same spine events.

```powershell
.venv\Scripts\activate
python examples/07-observer-presets/main.py
```

Inspect JSONL for `observer.note` and `observer.alert` after repeated `ping` calls.

→ [sequencer.md](../../docs/sequencer.md) · [reference-tool-host-capstone.md](../../docs/guides/reference-tool-host-capstone.md)
