from dataclasses import dataclass
from typing import Dict, List, Any, Optional
from typing_extensions import Self
from inflection import camelize, underscore
from .ProtocolMapperRepresentation import ProtocolMapperRepresentation


@dataclass
class ClientScopeRepresentation:
    id: Optional[str] = None
    name: Optional[str] = None
    description: Optional[str] = None
    protocol: Optional[str] = None
    attributes: Optional[Dict[str, Any]] = None
    protocol_mappers: Optional[List[ProtocolMapperRepresentation]] = None

    def to_dict(self) -> Dict[str, Any]:
        result: Dict[str, Any] = {}
        if self.id is not None:
            value = self.id
            result['id'] = value
        if self.name is not None:
            value = self.name
            result['name'] = value
        if self.description is not None:
            value = self.description
            result['description'] = value
        if self.protocol is not None:
            value = self.protocol
            result['protocol'] = value
        if self.attributes is not None:
            value = self.attributes
            result['attributes'] = value
        if self.protocol_mappers is not None:
            value = [item.to_dict() for item in self.protocol_mappers]
            result['protocolMappers'] = value
        return result

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> Self:
        snake_data: Dict[str, Any] = {underscore(k): v for k, v in data.items()}

        if 'protocol_mappers' in snake_data and snake_data['protocol_mappers'] is not None:
            snake_data['protocol_mappers'] = [
                ProtocolMapperRepresentation.from_dict(item) for item in snake_data['protocol_mappers']
            ]
        required_fields = []
        missing = [f for f in required_fields if f not in snake_data]
        if missing:
            raise ValueError(f'missing required field: {missing}')
        return cls(**snake_data)
