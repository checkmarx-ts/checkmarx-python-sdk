from dataclasses import dataclass
from typing import Optional


@dataclass
class DastLeanEnvironment:
    """An entry in `environments[]` on GET /leanEnvironments."""
    id: Optional[str] = None
    domain: Optional[str] = None
    environment_type: Optional[str] = None
    is_private: Optional[bool] = None
    has_tunnel: Optional[bool] = None
    is_auth_required: Optional[bool] = None
    is_authenticated: Optional[bool] = None

    @classmethod
    def from_dict(cls, item: dict) -> "DastLeanEnvironment":
        return cls(
            id=item.get("id"),
            domain=item.get("domain"),
            environment_type=item.get("environmentType"),
            is_private=item.get("isPrivate"),
            has_tunnel=item.get("hasTunnel"),
            is_auth_required=item.get("isAuthRequired"),
            is_authenticated=item.get("isAuthenticated"),
        )
