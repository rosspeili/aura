"""Real integration tests — require Skillware + Ollama; not run in default CI.

Run locally:
  .venv\\Scripts\\activate
  pip install -e ".[dev,integrations]"
  pytest tests/integration/ -v

CI excludes this directory via --ignore=tests/integration.
"""

from __future__ import annotations

import os
import urllib.error
import urllib.request
from pathlib import Path

import pytest

REPO_ROOT = Path(__file__).resolve().parents[2]


def ollama_api_ok() -> bool:
    base = os.environ.get("OLLAMA_BASE_URL", "http://127.0.0.1:11434").rstrip("/")
    try:
        with urllib.request.urlopen(f"{base}/api/tags", timeout=5) as response:
            return 200 <= response.status < 300
    except (urllib.error.URLError, OSError, TimeoutError):
        return False


@pytest.fixture(scope="session")
def require_skillware():
    pytest.importorskip("skillware")
    from aura.hosts import skillware_available

    if not skillware_available():
        pytest.fail("skillware extra required: pip install -e '.[skillware]'")


@pytest.fixture(scope="session")
def require_ollama():
    if not ollama_api_ok():
        pytest.fail("Ollama daemon not reachable — start `ollama serve` and pull llama3.2:1b")
    pytest.importorskip("ollama")


@pytest.fixture(scope="session")
def ollama_client(require_ollama):
    import ollama

    base = os.environ.get("OLLAMA_BASE_URL", "http://127.0.0.1:11434").rstrip("/")
    return ollama.Client(host=base)


@pytest.fixture(scope="session")
def ollama_model(require_ollama, ollama_client) -> str:
    model = os.environ.get("OLLAMA_MODEL", "llama3.2:1b")
    names = [m.model for m in ollama_client.list().models]
    if not any(model in name for name in names):
        pytest.fail(f"Model {model!r} not in Ollama: {names}")
    return model
