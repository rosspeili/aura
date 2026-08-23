"""Host bind helpers — ingress events when capabilities register on a session."""

from __future__ import annotations

from typing import Any

from aura.membrane.ingress import skill_registered_payload


def record_skill_bind(
    session: Any,
    *,
    skill_id: str,
    manifest_snapshot_hash: str,
    host_kind: str = "toolhost",
) -> None:
    """Emit skill.registered and optional first-time host.bind on the audit spine."""
    host_state = session.state.setdefault("host", {"kind": host_kind, "bound_skills": []})
    bound: list[str] = host_state.setdefault("bound_skills", [])
    first_bind = len(bound) == 0
    if skill_id not in bound:
        bound.append(skill_id)

    session.emit(
        "skill.registered",
        skill_registered_payload(
            session.profile,
            skill_id=skill_id,
            manifest_snapshot_hash=manifest_snapshot_hash,
            rule_count=len(session.rules),
            session_snapshot_hash=session.snapshot_hash,
            bound_skill_ids=list(bound),
        ),
    )

    if first_bind:
        session.emit(
            "host.bind",
            {
                "membrane": "ingress",
                "host_kind": host_kind,
                "session_snapshot_hash": session.snapshot_hash,
                "agent_ref": session.profile.agent_ref,
                "policy_version": session.profile.policy_version,
            },
        )
