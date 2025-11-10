from dataclasses import dataclass
from typing import Dict, List, Any, Optional
from typing_extensions import Self
from inflection import camelize, underscore
from .ClientPolicyExecutorRepresentation import ClientPolicyExecutorRepresentation


@dataclass
class ClientProfileRepresentation:
    name: Optional[str] = None
    description: Optional[str] = None
    executors: Optional[List[ClientPolicyExecutorRepresentation]] = None

    def to_dict(self) -> Dict[str, Any]:
        result: Dict[str, Any] = {}
        if self.name is not None:
            value = self.name
            result['name'] = value
        if self.description is not None:
            value = self.description
            result['description'] = value
        if self.executors is not None:
            value = [item.to_dict() for item in self.executors]
            result['executors'] = value
        return result

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> Self:
        snake_data: Dict[str, Any] = {underscore(k): v for k, v in data.items()}

        if 'executors' in snake_data and snake_data['executors'] is not None:
            snake_data['executors'] = [
                ClientPolicyExecutorRepresentation.from_dict(item) for item in snake_data['executors']
            ]
        required_fields = []
        missing = [f for f in required_fields if f not in snake_data]
        if missing:
            raise ValueError(f'missing required field: {missing}')
        return cls(**snake_data)
