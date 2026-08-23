# Skillware integration (reference adapter)

Reference **ToolHost** path under AURA — prescriptive sequencer, manifest merge at bind, egress policy, observers, session export.

| Artifact | Status |
|---|---|
| `SkillwareHost` | Shipped in `aura/hosts/skillware.py` |
| Mock-first demo | `examples/04-sequencer-pipeline/main.py` |
| Capstone script | Planned ([#40](https://github.com/ARPAHLS/aura/issues/40)) — `reference_tool_host.py` here |
| Live Skillware path | `pip install -e ".[skillware]"` — see [skillware-integration.md](../../docs/skillware-integration.md) |

AURA wraps Skillware at **egress**; swap `SkillwareHost` for another `ToolHost` implementation for other runtimes.

Parent epic: [#12](https://github.com/ARPAHLS/aura/issues/12).
