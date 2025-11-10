from dataclasses import dataclass
from typing import Dict, List, Any, Optional
from typing_extensions import Self
from inflection import camelize, underscore


@dataclass
class ClientPolicyConditionRepresentation:
    condition: Optional[str] = None
    configuration: Optional[List[Dict[str, Any]]] = None

    def to_dict(self) -> Dict[str, Any]:
        result: Dict[str, Any] = {}
        if self.condition is not None:
            value = self.condition
            result['condition'] = value
        if self.configuration is not None:
            value = self.configuration
            result['configuration'] = value
        return result

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> Self:
        snake_data: Dict[str, Any] = {underscore(k): v for k, v in data.items()}

        required_fields = []
        missing = [f for f in required_fields if f not in snake_data]
        if missing:
            raise ValueError(f'missing required field: {missing}')
        return cls(**snake_data)
