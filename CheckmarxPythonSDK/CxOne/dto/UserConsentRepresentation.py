from dataclasses import dataclass
from typing import List


@dataclass
class UserConsentRepresentation:
    client_id: str
    granted_client_scopes: List[str]
    created_date: int
    last_updated_date: int
    granted_realm_roles: List[str]
