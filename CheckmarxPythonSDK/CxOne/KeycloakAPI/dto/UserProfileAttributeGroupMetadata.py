from dataclasses import dataclass
from typing import Dict, List, Any, Optional
from typing_extensions import Self
from inflection import camelize, underscore


@dataclass
class UserProfileAttributeGroupMetadata:
    name: Optional[str] = None
    display_header: Optional[str] = None
    display_description: Optional[str] = None
    annotations: Optional[Dict[str, Any]] = None

    def to_dict(self) -> Dict[str, Any]:
        result: Dict[str, Any] = {}
        if self.name is not None:
            value = self.name
            result['name'] = value
        if self.display_header is not None:
            value = self.display_header
            result['displayHeader'] = value
        if self.display_description is not None:
            value = self.display_description
            result['displayDescription'] = value
        if self.annotations is not None:
            value = self.annotations
            result['annotations'] = value
        return result

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> Self:
        snake_data: Dict[str, Any] = {underscore(k): v for k, v in data.items()}

        required_fields = []
        missing = [f for f in required_fields if f not in snake_data]
        if missing:
            raise ValueError(f'missing required field: {missing}')
        return cls(**snake_data)
