from dataclasses import dataclass
from typing import Dict, List, Any, Optional
from typing_extensions import Self
from inflection import camelize, underscore
from .ConfigPropertyRepresentation import ConfigPropertyRepresentation


@dataclass
class IdentityProviderMapperTypeRepresentation:
    id: Optional[str] = None
    name: Optional[str] = None
    category: Optional[str] = None
    help_text: Optional[str] = None
    properties: Optional[List[ConfigPropertyRepresentation]] = None

    def to_dict(self) -> Dict[str, Any]:
        result: Dict[str, Any] = {}
        if self.id is not None:
            value = self.id
            result['id'] = value
        if self.name is not None:
            value = self.name
            result['name'] = value
        if self.category is not None:
            value = self.category
            result['category'] = value
        if self.help_text is not None:
            value = self.help_text
            result['helpText'] = value
        if self.properties is not None:
            value = [item.to_dict() for item in self.properties]
            result['properties'] = value
        return result

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> Self:
        snake_data: Dict[str, Any] = {underscore(k): v for k, v in data.items()}

        if 'properties' in snake_data and snake_data['properties'] is not None:
            snake_data['properties'] = [
                ConfigPropertyRepresentation.from_dict(item) for item in snake_data['properties']
            ]
        required_fields = []
        missing = [f for f in required_fields if f not in snake_data]
        if missing:
            raise ValueError(f'missing required field: {missing}')
        return cls(**snake_data)
