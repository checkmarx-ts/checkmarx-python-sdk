from dataclasses import dataclass
from typing import Dict, List, Any, Optional
from typing_extensions import Self
from inflection import camelize, underscore
from .RoleRepresentation import RoleRepresentation


@dataclass
class RolesRepresentation:
    realm: Optional[List[RoleRepresentation]] = None
    client: Optional[Dict[str, Any]] = None
    application: Optional[Dict[str, Any]] = None

    def to_dict(self) -> Dict[str, Any]:
        result: Dict[str, Any] = {}
        if self.realm is not None:
            value = [item.to_dict() for item in self.realm]
            result['realm'] = value
        if self.client is not None:
            value = self.client
            result['client'] = value
        if self.application is not None:
            value = self.application
            result['application'] = value
        return result

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> Self:
        snake_data: Dict[str, Any] = {underscore(k): v for k, v in data.items()}

        if 'realm' in snake_data and snake_data['realm'] is not None:
            snake_data['realm'] = [
                RoleRepresentation.from_dict(item) for item in snake_data['realm']
            ]
        required_fields = []
        missing = [f for f in required_fields if f not in snake_data]
        if missing:
            raise ValueError(f'missing required field: {missing}')
        return cls(**snake_data)
