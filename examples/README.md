# Examples

Runnable demos for AURA Harness.

| Example | Shows |
|---|---|
| [01-minimal-loop](01-minimal-loop/) | Auto agent ID, emit events, JSONL export |
| [02-guarded-tools](02-guarded-tools/) | Rules, approval gates, token limit |
| [03-task-mode](03-task-mode/) | Task mode, goal completion |
| [04-sequencer-pipeline](04-sequencer-pipeline/) | Sequencer + Skillware host (mock skills) |
| [05-skillware-skill-types](05-skillware-skill-types/) | Three Skillware categories (security, optimization, monitoring) |
| [06-skillware-sequencer-chain](06-skillware-sequencer-chain/) | Sequencer chain: scan → compress → budget |

```bash
pip install -e ..
cd examples/01-minimal-loop && python main.py
cd ../05-skillware-skill-types && python main.py
cd ../06-skillware-sequencer-chain && python main.py
```

Live Skillware registry skills: `$env:SKILLWARE_LIVE="1"` (PowerShell) before running 05 or 06.

Set `AURA_HOME` to isolate storage during tests.

→ Full Skillware guide: [docs/guides/aura-on-skillware.md](../docs/guides/aura-on-skillware.md)
