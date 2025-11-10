from dataclasses import dataclass
from typing import Dict, List, Any, Optional
from typing_extensions import Self
from inflection import camelize, underscore
from .UPAttributePermissions import UPAttributePermissions
from .UPAttributeRequired import UPAttributeRequired
from .UPAttributeSelector import UPAttributeSelector


@dataclass
class UPAttribute:
    name: Optional[str] = None
    display_name: Optional[str] = None
    validations: Optional[Dict[str, Any]] = None
    annotations: Optional[Dict[str, Any]] = None
    required: Optional[UPAttributeRequired] = None
    permissions: Optional[UPAttributePermissions] = None
    selector: Optional[UPAttributeSelector] = None
    group: Optional[str] = None

    def to_dict(self) -> Dict[str, Any]:
        result: Dict[str, Any] = {}
        if self.name is not None:
            value = self.name
            result['name'] = value
        if self.display_name is not None:
            value = self.display_name
            result['displayName'] = value
        if self.validations is not None:
            value = self.validations
            result['validations'] = value
        if self.annotations is not None:
            value = self.annotations
            result['annotations'] = value
        if self.required is not None:
            value = self.required.to_dict()
            result['required'] = value
        if self.permissions is not None:
            value = self.permissions.to_dict()
            result['permissions'] = value
        if self.selector is not None:
            value = self.selector.to_dict()
            result['selector'] = value
        if self.group is not None:
            value = self.group
            result['group'] = value
        return result

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> Self:
        snake_data: Dict[str, Any] = {underscore(k): v for k, v in data.items()}

        if 'required' in snake_data and snake_data['required'] is not None:
            snake_data['required'] = UPAttributeRequired.from_dict(snake_data['required'])
        if 'permissions' in snake_data and snake_data['permissions'] is not None:
            snake_data['permissions'] = UPAttributePermissions.from_dict(snake_data['permissions'])
        if 'selector' in snake_data and snake_data['selector'] is not None:
            snake_data['selector'] = UPAttributeSelector.from_dict(snake_data['selector'])
        required_fields = []
        missing = [f for f in required_fields if f not in snake_data]
        if missing:
            raise ValueError(f'missing required field: {missing}')
        return cls(**snake_data)
