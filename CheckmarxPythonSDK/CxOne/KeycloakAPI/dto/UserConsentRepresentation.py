from dataclasses import dataclass
from typing import Dict, List, Any, Optional
from typing_extensions import Self
from inflection import camelize, underscore


@dataclass
class UserConsentRepresentation:
    client_id: Optional[str] = None
    granted_client_scopes: Optional[List[str]] = None
    created_date: Optional[int] = None
    last_updated_date: Optional[int] = None
    granted_realm_roles: Optional[List[str]] = None

    def to_dict(self) -> Dict[str, Any]:
        result: Dict[str, Any] = {}
        if self.client_id is not None:
            value = self.client_id
            result['clientId'] = value
        if self.granted_client_scopes is not None:
            value = self.granted_client_scopes
            result['grantedClientScopes'] = value
        if self.created_date is not None:
            value = self.created_date
            result['createdDate'] = value
        if self.last_updated_date is not None:
            value = self.last_updated_date
            result['lastUpdatedDate'] = value
        if self.granted_realm_roles is not None:
            value = self.granted_realm_roles
            result['grantedRealmRoles'] = value
        return result

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> Self:
        snake_data: Dict[str, Any] = {underscore(k): v for k, v in data.items()}

        required_fields = []
        missing = [f for f in required_fields if f not in snake_data]
        if missing:
            raise ValueError(f'missing required field: {missing}')
        return cls(**snake_data)
