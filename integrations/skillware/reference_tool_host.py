#!/usr/bin/env python3
"""
Reference tool-host pipeline — mock by default, live Skillware when SKILLWARE_LIVE=1.

From repo root:
  pip install -e ".[dev,skillware]"
  python integrations/skillware/reference_tool_host.py

Live path (offline skills, no API keys):
  set SKILLWARE_LIVE=1
  python integrations/skillware/reference_tool_host.py
"""

from __future__ import annotations

import json
import os
import sys
from pathlib import Path

_REPO_ROOT = Path(__file__).resolve().parents[2]
if str(_REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(_REPO_ROOT))

from aura import agent, configure  # noqa: E402
from aura.hosts import MockSkill, SkillwareHost, skillware_available  # noqa: E402


def _load_env() -> None:
    env_path = _REPO_ROOT / ".env"
    if not env_path.is_file():
        return
    for line in env_path.read_text(encoding="utf-8").splitlines():
        line = line.strip()
        if not line or line.startswith("#") or "=" not in line:
            continue
        key, _, value = line.partition("=")
        os.environ.setdefault(key.strip(), value.strip())


def run_mock(host: SkillwareHost) -> dict:
    host.register(
        MockSkill(
            "optimization/prompt_rewriter",
            {"execute": lambda a: {"compressed_text": str(a.get("raw_text", ""))[:40]}},
        )
    )
    return host.execute(
        "optimization/prompt_rewriter",
        "execute",
        {
            "raw_text": "Please kindly ensure you read this entirely.",
            "compression_aggression": "medium",
        },
    )


def run_live(host: SkillwareHost) -> dict:
    if not skillware_available():
        raise RuntimeError("skillware extra not installed — pip install -e '.[skillware]'")
    skill = host.register_registry_skill("optimization/prompt_rewriter")
    return host.execute(
        skill.skill_id,
        skill.skill_id,
        {
            "raw_text": "Please kindly ensure you read this entirely.",
            "compression_aggression": "high",
        },
    )


def main() -> None:
    _load_env()
    configure()
    live = os.environ.get("SKILLWARE_LIVE", "").strip().lower() in ("1", "true", "yes")
    mode = "live" if live else "mock"

    ag = agent(
        "reference-tool-host",
        purpose="Demonstrate ToolHost + membrane egress with Skillware reference adapter",
        skills=["optimization/prompt_rewriter"],
    )

    with ag.session(mode="script") as run:
        host = SkillwareHost(run._session)
        if live:
            result = run_live(host)
        else:
            result = run_mock(host)
        run.emit("turn.end", {"output": "reference pipeline complete", "mode": mode})

    print(json.dumps({"mode": mode, "result": result, "session_id": run.session_id}, indent=2))
    print(f"exports: {run.exports}")


if __name__ == "__main__":
    main()
