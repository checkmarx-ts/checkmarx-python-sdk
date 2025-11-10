from dataclasses import dataclass
from typing import Dict, List, Any, Optional
from typing_extensions import Self
from inflection import camelize, underscore


@dataclass
class ConfigPropertyRepresentation:
    name: Optional[str] = None
    label: Optional[str] = None
    help_text: Optional[str] = None
    type: Optional[str] = None
    default_value: Optional[Dict[str, Any]] = None
    options: Optional[List[str]] = None
    secret: Optional[bool] = None
    required: Optional[bool] = None
    read_only: Optional[bool] = None

    def to_dict(self) -> Dict[str, Any]:
        result: Dict[str, Any] = {}
        if self.name is not None:
            value = self.name
            result['name'] = value
        if self.label is not None:
            value = self.label
            result['label'] = value
        if self.help_text is not None:
            value = self.help_text
            result['helpText'] = value
        if self.type is not None:
            value = self.type
            result['type'] = value
        if self.default_value is not None:
            value = self.default_value
            result['defaultValue'] = value
        if self.options is not None:
            value = self.options
            result['options'] = value
        if self.secret is not None:
            value = self.secret
            result['secret'] = value
        if self.required is not None:
            value = self.required
            result['required'] = value
        if self.read_only is not None:
            value = self.read_only
            result['readOnly'] = value
        return result

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> Self:
        snake_data: Dict[str, Any] = {underscore(k): v for k, v in data.items()}

        required_fields = []
        missing = [f for f in required_fields if f not in snake_data]
        if missing:
            raise ValueError(f'missing required field: {missing}')
        return cls(**snake_data)
