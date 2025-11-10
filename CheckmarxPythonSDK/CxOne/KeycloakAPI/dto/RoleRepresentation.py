from dataclasses import dataclass
from typing import Dict, List, Any, Optional
from typing_extensions import Self
from inflection import camelize, underscore
from .Composites import Composites


@dataclass
class RoleRepresentation:
    id: Optional[str] = None
    name: Optional[str] = None
    description: Optional[str] = None
    scope_param_required: Optional[bool] = None
    composite: Optional[bool] = None
    composites: Optional[Composites] = None
    client_role: Optional[bool] = None
    container_id: Optional[str] = None
    attributes: Optional[Dict[str, Any]] = None

    def to_dict(self) -> Dict[str, Any]:
        result: Dict[str, Any] = {}
        if self.id is not None:
            value = self.id
            result['id'] = value
        if self.name is not None:
            value = self.name
            result['name'] = value
        if self.description is not None:
            value = self.description
            result['description'] = value
        if self.scope_param_required is not None:
            value = self.scope_param_required
            result['scopeParamRequired'] = value
        if self.composite is not None:
            value = self.composite
            result['composite'] = value
        if self.composites is not None:
            value = self.composites.to_dict()
            result['composites'] = value
        if self.client_role is not None:
            value = self.client_role
            result['clientRole'] = value
        if self.container_id is not None:
            value = self.container_id
            result['containerId'] = value
        if self.attributes is not None:
            value = self.attributes
            result['attributes'] = value
        return result

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> Self:
        snake_data: Dict[str, Any] = {underscore(k): v for k, v in data.items()}

        if 'composites' in snake_data and snake_data['composites'] is not None:
            snake_data['composites'] = Composites.from_dict(snake_data['composites'])
        required_fields = []
        missing = [f for f in required_fields if f not in snake_data]
        if missing:
            raise ValueError(f'missing required field: {missing}')
        return cls(**snake_data)
