from dataclasses import dataclass
from typing import Optional


@dataclass
class CxLink:
    """A Checkmarx Link (GET /api/v1/link/links/{id}) -- the tunnel used to
    reach a private, on-premises SCM from the CxOne tenant.
    """
    id: Optional[str] = None
    name: Optional[str] = None
    description: Optional[str] = None
    private_url: Optional[str] = None
    link_url: Optional[str] = None
    state: Optional[str] = None  # e.g. connected
    client_type: Optional[str] = None  # e.g. docker
    client_version: Optional[str] = None
    client_private_url: Optional[str] = None
    created_at: Optional[str] = None

    @classmethod
    def from_dict(cls, item: dict) -> "CxLink":
        return cls(
            id=item.get("id"),
            name=item.get("name"),
            description=item.get("description"),
            private_url=item.get("privateUrl"),
            link_url=item.get("linkUrl"),
            state=item.get("state"),
            client_type=item.get("clientType"),
            client_version=item.get("clientVersion"),
            client_private_url=item.get("clientPrivateUrl"),
            created_at=item.get("createdAt"),
        )
