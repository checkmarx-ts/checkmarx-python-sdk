from dataclasses import dataclass


@dataclass
class PresetSummary:
    id: int = None
    name: str = None
    description: str = None
    associated_projects: int = None
    custom: bool = None
    is_tenant_default: bool = None
    is_migrated: bool = None

    @classmethod
    def from_dict(cls, item: dict) -> "PresetSummary":
        return cls(
            id=item.get("id"),
            name=item.get("name"),
            description=item.get("description"),
            associated_projects=item.get("associatedProjects"),
            custom=item.get("custom"),
            is_tenant_default=item.get("isTenantDefault"),
            is_migrated=item.get("isMigrated"),
        )
