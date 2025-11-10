from dataclasses import dataclass
from typing import Dict, List, Any, Optional
from typing_extensions import Self
from inflection import camelize, underscore


# from .PolicyRepresentation import PolicyRepresentation
# from .ResourceRepresentation import ResourceRepresentation


@dataclass
class ScopeRepresentation:
    id: Optional[str] = None
    name: Optional[str] = None
    icon_uri: Optional[str] = None
    # policies: Optional[List[PolicyRepresentation]] = None
    # resources: Optional[List[ResourceRepresentation]] = None
    display_name: Optional[str] = None

    def to_dict(self) -> Dict[str, Any]:
        result: Dict[str, Any] = {}
        if self.id is not None:
            value = self.id
            result['id'] = value
        if self.name is not None:
            value = self.name
            result['name'] = value
        if self.icon_uri is not None:
            value = self.icon_uri
            result['iconUri'] = value
        # if self.policies is not None:
        #     value = [item.to_dict() for item in self.policies]
        #     result['policies'] = value
        # if self.resources is not None:
        #     value = [item.to_dict() for item in self.resources]
        #     result['resources'] = value
        if self.display_name is not None:
            value = self.display_name
            result['displayName'] = value
        return result

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> Self:
        snake_data: Dict[str, Any] = {underscore(k): v for k, v in data.items()}

        # if 'policies' in snake_data and snake_data['policies'] is not None:
        #     snake_data['policies'] = [
        #         PolicyRepresentation.from_dict(item) for item in snake_data['policies']
        #     ]
        # if 'resources' in snake_data and snake_data['resources'] is not None:
        #     snake_data['resources'] = [
        #         ResourceRepresentation.from_dict(item) for item in snake_data['resources']
        #     ]
        required_fields = []
        missing = [f for f in required_fields if f not in snake_data]
        if missing:
            raise ValueError(f'missing required field: {missing}')
        return cls(**snake_data)
