from dataclasses import dataclass, field
from typing import List, Optional


@dataclass
class DastApplicationEnvironmentWithPrimary:
    """An entry in the response of GET /associatedApps/{envId} -- an
    Application associated with a DAST Environment."""
    id: Optional[str] = None
    name: Optional[str] = None
    criticality: Optional[int] = None
    project_ids: List[str] = field(default_factory=list)
    is_primary: Optional[bool] = None

    @classmethod
    def from_dict(cls, item: dict) -> "DastApplicationEnvironmentWithPrimary":
        return cls(
            id=item.get("id"),
            name=item.get("name"),
            criticality=item.get("criticality"),
            project_ids=list(item.get("projectIds") or []),
            is_primary=item.get("isPrimary"),
        )
