# Example 08 — Emit-only loop (loose coat)

AURA as **audit membrane only** — no `ToolHost`, no skill runtime. You `emit()` what matters at boundaries; session export on close.

Use when:

- Prototyping a body loop before wiring tool egress
- Logging model turns without capability enforcement yet
- Comparing against tight coat runs that route every tool through `host.execute()`

```powershell
.venv\Scripts\activate
python examples/08-emit-only-loop/main.py
```

→ [using-aura.md](../../docs/using-aura.md) · [reference-tool-host-capstone.md](../../docs/guides/reference-tool-host-capstone.md)
