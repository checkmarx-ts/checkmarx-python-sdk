from dataclasses import dataclass
from typing import List


@dataclass
class UserConsentRepresentation:
    client_id: str
    granted_client_scopes: List[str]
    created_date: int
    last_updated_date: int
    granted_realm_roles: List[str]

    def to_dict(self):
        return {
            "clientId": self.client_id,
            "grantedClientScopes": self.granted_client_scopes,
            "createdDate": self.created_date,
            "lastUpdatedDate": self.last_updated_date,
            "grantedRealmRoles": self.granted_realm_roles,
        }


def construct_user_consent_representation(item):
    return UserConsentRepresentation(
        client_id=item.get("clientId"),
        granted_client_scopes=item.get("grantedClientScopes"),
        created_date=item.get("createdDate"),
        last_updated_date=item.get("lastUpdatedDate"),
        granted_realm_roles=item.get("grantedRealmRoles"),
    )
