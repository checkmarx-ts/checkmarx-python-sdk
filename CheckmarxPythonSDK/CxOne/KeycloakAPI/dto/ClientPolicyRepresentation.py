from dataclasses import dataclass
from typing import Dict, List, Any, Optional
from typing_extensions import Self
from inflection import camelize, underscore
from .ClientPolicyConditionRepresentation import ClientPolicyConditionRepresentation


@dataclass
class ClientPolicyRepresentation:
    name: Optional[str] = None
    description: Optional[str] = None
    enabled: Optional[bool] = None
    conditions: Optional[List[ClientPolicyConditionRepresentation]] = None
    profiles: Optional[List[str]] = None

    def to_dict(self) -> Dict[str, Any]:
        result: Dict[str, Any] = {}
        if self.name is not None:
            value = self.name
            result['name'] = value
        if self.description is not None:
            value = self.description
            result['description'] = value
        if self.enabled is not None:
            value = self.enabled
            result['enabled'] = value
        if self.conditions is not None:
            value = [item.to_dict() for item in self.conditions]
            result['conditions'] = value
        if self.profiles is not None:
            value = self.profiles
            result['profiles'] = value
        return result

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> Self:
        snake_data: Dict[str, Any] = {underscore(k): v for k, v in data.items()}

        if 'conditions' in snake_data and snake_data['conditions'] is not None:
            snake_data['conditions'] = [
                ClientPolicyConditionRepresentation.from_dict(item) for item in snake_data['conditions']
            ]
        required_fields = []
        missing = [f for f in required_fields if f not in snake_data]
        if missing:
            raise ValueError(f'missing required field: {missing}')
        return cls(**snake_data)
