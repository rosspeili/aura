"""Skill manifest → session constraint rules (host bind)."""

from __future__ import annotations

from hashlib import sha256
import json
from typing import Any


def manifest_to_rules(manifest: dict[str, Any]) -> list[dict[str, Any]]:
    """Convert a skill manifest guardrails block into declarative constraint rules."""
    if not manifest:
        return []
    rules: list[dict[str, Any]] = []
    guardrails = (
        manifest.get("guardrails") if isinstance(manifest.get("guardrails"), dict) else manifest
    )

    allow = guardrails.get("allow_tools") or guardrails.get("allow")
    if allow:
        rules.append({"type": "allow_tools", "tools": list(allow)})

    deny = guardrails.get("deny_tools") or guardrails.get("deny")
    if deny:
        rules.append({"type": "deny_tools", "tools": list(deny)})

    confirm = guardrails.get("confirm_before")
    if confirm:
        tools = confirm.get("tools") if isinstance(confirm, dict) else confirm
        if tools:
            rules.append({"type": "confirm_before", "tools": list(tools)})

    limit = guardrails.get("max_tokens_per_step") or guardrails.get("max_tokens")
    if limit is not None:
        rules.append({"type": "max_tokens_per_step", "limit": int(limit)})

    return rules


def manifest_snapshot_hash(skill_id: str, manifest: dict[str, Any]) -> str:
    blob = json.dumps({"skill_id": skill_id, "manifest": manifest}, sort_keys=True)
    return sha256(blob.encode()).hexdigest()[:16]


def merge_manifest_into_rules(
    rules: list[dict[str, Any]],
    skill_id: str,
    manifest: dict[str, Any],
) -> list[dict[str, Any]]:
    """Append manifest-derived rules; tag each with bind metadata for audit."""
    merged = list(rules)
    for rule in manifest_to_rules(manifest):
        tagged = dict(rule)
        tagged["_bind"] = {"skill_id": skill_id, "source": "manifest"}
        merged.append(tagged)
    return merged
