from dataclasses import dataclass
from typing import Dict, List, Any, Optional
from typing_extensions import Self
from inflection import camelize, underscore


@dataclass
class UserProfileAttributeMetadata:
    name: Optional[str] = None
    display_name: Optional[str] = None
    required: Optional[bool] = None
    read_only: Optional[bool] = None
    annotations: Optional[Dict[str, Any]] = None
    validators: Optional[Dict[str, Any]] = None
    group: Optional[str] = None
    multivalued: Optional[bool] = None

    def to_dict(self) -> Dict[str, Any]:
        result: Dict[str, Any] = {}
        if self.name is not None:
            value = self.name
            result['name'] = value
        if self.display_name is not None:
            value = self.display_name
            result['displayName'] = value
        if self.required is not None:
            value = self.required
            result['required'] = value
        if self.read_only is not None:
            value = self.read_only
            result['readOnly'] = value
        if self.annotations is not None:
            value = self.annotations
            result['annotations'] = value
        if self.validators is not None:
            value = self.validators
            result['validators'] = value
        if self.group is not None:
            value = self.group
            result['group'] = value
        if self.multivalued is not None:
            value = self.multivalued
            result['multivalued'] = value
        return result

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> Self:
        snake_data: Dict[str, Any] = {underscore(k): v for k, v in data.items()}

        required_fields = []
        missing = [f for f in required_fields if f not in snake_data]
        if missing:
            raise ValueError(f'missing required field: {missing}')
        return cls(**snake_data)
