from dataclasses import dataclass


@dataclass
class PresetSummary:
    """

    Attributes:
        id (int):
        name (str):
        description (str):
        associated_projects (int):
        custom (bool):
        is_tenant_default (bool):
        is_migrated (bool):
    """
    id: int = None
    name: str = None
    description: str = None
    associated_projects: int = None
    custom: bool = None,
    is_tenant_default: bool = None
    is_migrated: bool = None


def construct_preset_summary(item):
    return PresetSummary(
        id=item.get("id"),
        name=item.get("name"),
        description=item.get("description"),
        associated_projects=item.get("associatedProjects"),
        custom=item.get("custom"),
        is_tenant_default=item.get("isTenantDefault"),
        is_migrated=item.get("isMigrated")
    )
