from dataclasses import dataclass


@dataclass
class DefaultConfigOut:
    id: str = None
    name: str = None
    description: str = None
    url: str = None
    is_tenant_default: bool = None
    associated_projects: int = None

    @classmethod
    def from_dict(cls, item: dict) -> "DefaultConfigOut":
        return cls(
            id=item.get("id"),
            name=item.get("name"),
            description=item.get("description"),
            url=item.get("url"),
            is_tenant_default=item.get("isTenantDefault"),
            associated_projects=item.get("associatedProjects"),
        )
