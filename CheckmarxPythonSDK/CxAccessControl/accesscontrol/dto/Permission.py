from dataclasses import dataclass
from typing import Optional


@dataclass
class Permission:
    id: Optional[int] = None
    service_provider_id: Optional[int] = None
    name: Optional[str] = None
    category: Optional[str] = None

    @classmethod
    def from_dict(cls, item: dict) -> "Permission":
        return cls(
            id=item.get("id"),
            service_provider_id=item.get("serviceProviderId"),
            name=item.get("name"),
            category=item.get("category"),
        )
