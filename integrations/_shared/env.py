"""Shared helpers for integration scripts (env loading, repo root)."""

from __future__ import annotations

import os
import sys
from pathlib import Path


def repo_root(start: Path | None = None) -> Path:
    """Repository root (parent of ``integrations/``)."""
    if start is None:
        start = Path(__file__).resolve()
    return start.parents[2]


def ensure_repo_on_path(root: Path | None = None) -> Path:
    root = root or repo_root()
    root_str = str(root)
    if root_str not in sys.path:
        sys.path.insert(0, root_str)
    return root


def load_dotenv(root: Path | None = None) -> None:
    """Load ``.env`` from repo root into ``os.environ`` (setdefault only)."""
    root = root or repo_root()
    env_path = root / ".env"
    if not env_path.is_file():
        return
    for line in env_path.read_text(encoding="utf-8").splitlines():
        line = line.strip()
        if not line or line.startswith("#") or "=" not in line:
            continue
        key, _, value = line.partition("=")
        os.environ.setdefault(key.strip(), value.strip())


def skillware_live() -> bool:
    return os.environ.get("SKILLWARE_LIVE", "").strip().lower() in ("1", "true", "yes")
