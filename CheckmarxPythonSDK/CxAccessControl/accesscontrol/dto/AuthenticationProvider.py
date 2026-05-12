from dataclasses import dataclass
from typing import Optional


@dataclass
class AuthenticationProvider:
    id: Optional[int] = None
    name: Optional[str] = None
    provider_id: Optional[int] = None
    provider_type: Optional[str] = None
    is_external: Optional[bool] = None
    active: Optional[bool] = None

    @classmethod
    def from_dict(cls, item: dict) -> "AuthenticationProvider":
        return cls(
            id=item.get("id"),
            name=item.get("name"),
            provider_id=item.get("providerId"),
            provider_type=item.get("providerType"),
            is_external=item.get("isExternal"),
            active=item.get("active"),
        )
