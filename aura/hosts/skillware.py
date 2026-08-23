"""Skillware host — wrap Skillware execute() through the membrane egress."""

from __future__ import annotations

from typing import Any

from aura.hosts.manifest import manifest_snapshot_hash, merge_manifest_into_rules
from aura.hosts.protocol import SkillExecutor
from aura.membrane.egress import guarded_tool_call
from aura.membrane.ingress import skill_registered_payload


class SkillwareHost:
    """
    Reference ToolHost adapter for Skillware skills.
    All tool execution passes through AURA egress (policy + audit).
    """

    def __init__(self, session: Any) -> None:
        self.session = session
        self._skills: dict[str, SkillExecutor] = {}

    def register(self, skill: SkillExecutor) -> None:
        self._skills[skill.skill_id] = skill
        manifest = getattr(skill, "manifest", None)
        if isinstance(manifest, dict) and manifest:
            self._bind_manifest(skill.skill_id, manifest)

    def register_by_id(self, skill_id: str, skill: Any) -> None:
        """Wrap a raw Skillware skill instance."""
        wrapped = _wrap_skillware_instance(skill_id, skill)
        manifest = getattr(skill, "manifest", None)
        if isinstance(manifest, dict):
            wrapped.manifest = manifest  # type: ignore[attr-defined]
        self.register(wrapped)

    def execute(
        self,
        skill_id: str,
        tool: str,
        args: dict[str, Any] | None = None,
        *,
        step_id: str | None = None,
    ) -> Any:
        skill = self._skills.get(skill_id)
        if skill is None:
            raise KeyError(f"Skill not registered: {skill_id}")

        def run() -> Any:
            return skill.execute(tool, args)

        return guarded_tool_call(
            self.session,
            tool=tool,
            skill_id=skill_id,
            args=args,
            execute=run,
            step_id=step_id,
        )

    @classmethod
    def from_skillware(cls, session: Any, skills: list[Any]) -> "SkillwareHost":
        """Build host from installed Skillware skill instances."""
        host = cls(session)
        for skill in skills:
            skill_id = getattr(skill, "skill_id", None) or getattr(
                skill, "id", type(skill).__name__
            )
            host.register_by_id(str(skill_id), skill)
        return host

    def _bind_manifest(self, skill_id: str, manifest: dict[str, Any]) -> None:
        session = self.session
        session.rules = merge_manifest_into_rules(session.rules, skill_id, manifest)
        snapshot = manifest_snapshot_hash(skill_id, manifest)
        session.snapshot_hash = _recompute_snapshot_hash(session)
        session.emit(
            "skill.registered",
            skill_registered_payload(
                session.profile,
                skill_id=skill_id,
                manifest_snapshot_hash=snapshot,
                rule_count=len(session.rules),
            ),
        )


def _wrap_skillware_instance(skill_id: str, skill: Any) -> SkillExecutor:
    class _Wrapped:
        def __init__(self) -> None:
            self.skill_id = skill_id
            self._skill = skill
            self.manifest: dict[str, Any] = {}

        def execute(self, tool: str, args: dict[str, Any] | None = None) -> Any:
            payload = dict(args or {})
            if hasattr(self._skill, "execute"):
                return self._skill.execute(tool, **payload)
            if hasattr(self._skill, "run"):
                return self._skill.run(tool, **payload)
            raise AttributeError(f"Skill {skill_id} has no execute/run method")

    return _Wrapped()


def _recompute_snapshot_hash(session: Any) -> str:
    from aura.core.session import _snapshot_hash

    return _snapshot_hash(session.profile, session.rules)


def skillware_available() -> bool:
    try:
        import skillware  # noqa: F401

        return True
    except ImportError:
        return False
