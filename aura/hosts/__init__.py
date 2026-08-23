"""Host adapters — ToolHost protocol, Skillware reference, mock skills."""

from aura.hosts.manifest import manifest_snapshot_hash, manifest_to_rules, merge_manifest_into_rules
from aura.hosts.mock import MockSkill, MockSkillRegistry
from aura.hosts.protocol import SkillExecutor, ToolHost
from aura.hosts.skillware import SkillwareHost, skillware_available
from aura.hosts.skillware_adapter import (
    SkillwareRegistrySkill,
    load_registry_skill,
    load_registry_skills,
)

__all__ = [
    "MockSkill",
    "MockSkillRegistry",
    "SkillExecutor",
    "SkillwareHost",
    "SkillwareRegistrySkill",
    "ToolHost",
    "load_registry_skill",
    "load_registry_skills",
    "manifest_snapshot_hash",
    "manifest_to_rules",
    "merge_manifest_into_rules",
    "skillware_available",
]
