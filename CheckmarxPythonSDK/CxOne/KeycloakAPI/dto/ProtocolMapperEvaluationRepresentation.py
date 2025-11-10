from dataclasses import dataclass
from typing import Dict, List, Any, Optional
from typing_extensions import Self
from inflection import camelize, underscore


@dataclass
class ProtocolMapperEvaluationRepresentation:
    mapper_id: Optional[str] = None
    mapper_name: Optional[str] = None
    container_id: Optional[str] = None
    container_name: Optional[str] = None
    container_type: Optional[str] = None
    protocol_mapper: Optional[str] = None

    def to_dict(self) -> Dict[str, Any]:
        result: Dict[str, Any] = {}
        if self.mapper_id is not None:
            value = self.mapper_id
            result['mapperId'] = value
        if self.mapper_name is not None:
            value = self.mapper_name
            result['mapperName'] = value
        if self.container_id is not None:
            value = self.container_id
            result['containerId'] = value
        if self.container_name is not None:
            value = self.container_name
            result['containerName'] = value
        if self.container_type is not None:
            value = self.container_type
            result['containerType'] = value
        if self.protocol_mapper is not None:
            value = self.protocol_mapper
            result['protocolMapper'] = value
        return result

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> Self:
        snake_data: Dict[str, Any] = {underscore(k): v for k, v in data.items()}

        required_fields = []
        missing = [f for f in required_fields if f not in snake_data]
        if missing:
            raise ValueError(f'missing required field: {missing}')
        return cls(**snake_data)
