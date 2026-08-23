# Examples

Runnable demos for AURA Harness.

| Example | Shows |
|---|---|
| [01-minimal-loop](01-minimal-loop/) | Auto agent ID, emit events, JSONL export |
| [02-guarded-tools](02-guarded-tools/) | Rules, approval gates, token limit |
| [03-task-mode](03-task-mode/) | Task mode, goal completion |
| [04-sequencer-pipeline](04-sequencer-pipeline/) | Sequencer + Skillware host (mock skills) |
| [05-skillware-skill-types](05-skillware-skill-types/) | Three Skillware categories (security, optimization, monitoring) |
| [06-skillware-sequencer-chain](06-skillware-sequencer-chain/) | Sequencer chain with conditional `when` steps |
| [07-observer-presets](07-observer-presets/) | Monitor + Break observer presets on ToolHost |
| [08-emit-only-loop](08-emit-only-loop/) | Loose coat — emit-only, no tool host |

```bash
pip install -e ..
cd examples/01-minimal-loop && python main.py
cd ../07-observer-presets && python main.py
```

Live registry skills (examples 05–06): `$env:SKILLWARE_LIVE="1"` (PowerShell).

Set `AURA_HOME` to isolate storage during tests.

→ Capstone checklist: [docs/guides/reference-tool-host-capstone.md](../docs/guides/reference-tool-host-capstone.md)
