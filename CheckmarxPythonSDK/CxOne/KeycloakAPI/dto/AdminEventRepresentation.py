from dataclasses import dataclass
from typing import Dict, List, Any, Optional
from typing_extensions import Self
from inflection import camelize, underscore
from .AuthDetailsRepresentation import AuthDetailsRepresentation


@dataclass
class AdminEventRepresentation:
    time: Optional[int] = None
    realm_id: Optional[str] = None
    auth_details: Optional[AuthDetailsRepresentation] = None
    operation_type: Optional[str] = None
    resource_type: Optional[str] = None
    resource_path: Optional[str] = None
    representation: Optional[str] = None
    error: Optional[str] = None

    def to_dict(self) -> Dict[str, Any]:
        result: Dict[str, Any] = {}
        if self.time is not None:
            value = self.time
            result['time'] = value
        if self.realm_id is not None:
            value = self.realm_id
            result['realmId'] = value
        if self.auth_details is not None:
            value = self.auth_details.to_dict()
            result['authDetails'] = value
        if self.operation_type is not None:
            value = self.operation_type
            result['operationType'] = value
        if self.resource_type is not None:
            value = self.resource_type
            result['resourceType'] = value
        if self.resource_path is not None:
            value = self.resource_path
            result['resourcePath'] = value
        if self.representation is not None:
            value = self.representation
            result['representation'] = value
        if self.error is not None:
            value = self.error
            result['error'] = value
        return result

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> Self:
        snake_data: Dict[str, Any] = {underscore(k): v for k, v in data.items()}

        if 'auth_details' in snake_data and snake_data['auth_details'] is not None:
            snake_data['auth_details'] = AuthDetailsRepresentation.from_dict(snake_data['auth_details'])
        required_fields = []
        missing = [f for f in required_fields if f not in snake_data]
        if missing:
            raise ValueError(f'missing required field: {missing}')
        return cls(**snake_data)
