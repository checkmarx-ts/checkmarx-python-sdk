from dataclasses import dataclass
from typing import Dict, List, Any, Optional
from typing_extensions import Self
from inflection import camelize, underscore
from .ClientPolicyRepresentation import ClientPolicyRepresentation


@dataclass
class ClientPoliciesRepresentation:
    policies: Optional[List[ClientPolicyRepresentation]] = None

    def to_dict(self) -> Dict[str, Any]:
        result: Dict[str, Any] = {}
        if self.policies is not None:
            value = [item.to_dict() for item in self.policies]
            result['policies'] = value
        return result

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> Self:
        snake_data: Dict[str, Any] = {underscore(k): v for k, v in data.items()}

        if 'policies' in snake_data and snake_data['policies'] is not None:
            snake_data['policies'] = [
                ClientPolicyRepresentation.from_dict(item) for item in snake_data['policies']
            ]
        required_fields = []
        missing = [f for f in required_fields if f not in snake_data]
        if missing:
            raise ValueError(f'missing required field: {missing}')
        return cls(**snake_data)
