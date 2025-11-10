from dataclasses import dataclass
from typing import Dict, List, Any, Optional
from typing_extensions import Self
from inflection import camelize, underscore
from .RoleRepresentation import RoleRepresentation


@dataclass
class ClientMappingsRepresentation:
    id: Optional[str] = None
    client: Optional[str] = None
    mappings: Optional[List[RoleRepresentation]] = None

    def to_dict(self) -> Dict[str, Any]:
        result: Dict[str, Any] = {}
        if self.id is not None:
            value = self.id
            result['id'] = value
        if self.client is not None:
            value = self.client
            result['client'] = value
        if self.mappings is not None:
            value = [item.to_dict() for item in self.mappings]
            result['mappings'] = value
        return result

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> Self:
        snake_data: Dict[str, Any] = {underscore(k): v for k, v in data.items()}

        if 'mappings' in snake_data and snake_data['mappings'] is not None:
            snake_data['mappings'] = [
                RoleRepresentation.from_dict(item) for item in snake_data['mappings']
            ]
        required_fields = []
        missing = [f for f in required_fields if f not in snake_data]
        if missing:
            raise ValueError(f'missing required field: {missing}')
        return cls(**snake_data)
