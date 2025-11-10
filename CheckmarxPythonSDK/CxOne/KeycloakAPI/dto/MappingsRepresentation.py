from dataclasses import dataclass
from typing import Dict, List, Any, Optional
from typing_extensions import Self
from inflection import camelize, underscore
from .RoleRepresentation import RoleRepresentation


@dataclass
class MappingsRepresentation:
    realm_mappings: Optional[List[RoleRepresentation]] = None
    client_mappings: Optional[Dict[str, Any]] = None

    def to_dict(self) -> Dict[str, Any]:
        result: Dict[str, Any] = {}
        if self.realm_mappings is not None:
            value = [item.to_dict() for item in self.realm_mappings]
            result['realmMappings'] = value
        if self.client_mappings is not None:
            value = self.client_mappings
            result['clientMappings'] = value
        return result

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> Self:
        snake_data: Dict[str, Any] = {underscore(k): v for k, v in data.items()}

        if 'realm_mappings' in snake_data and snake_data['realm_mappings'] is not None:
            snake_data['realm_mappings'] = [
                RoleRepresentation.from_dict(item) for item in snake_data['realm_mappings']
            ]
        required_fields = []
        missing = [f for f in required_fields if f not in snake_data]
        if missing:
            raise ValueError(f'missing required field: {missing}')
        return cls(**snake_data)
