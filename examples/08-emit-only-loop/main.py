"""Example 08 — Loose coat: emit-only loop without a ToolHost."""

from __future__ import annotations

import json

from aura import agent, configure


def main() -> None:
    configure()
    ag = agent(
        "emit-only-demo",
        agent_ref="demo/emit-only",
        purpose="Audit trail without tool egress — manual boundary emits",
    )

    with ag.session(mode="script") as run:
        run.emit("turn.start", {"input": "operator question"})
        run.emit("model.call", {"provider": "local", "model": "stub", "output": "draft answer"})
        run.emit("turn.end", {"output": "complete", "note": "no tool host wired"})

    print(json.dumps({"session_id": run.session_id, "exports": run.exports}, indent=2))


if __name__ == "__main__":
    main()
