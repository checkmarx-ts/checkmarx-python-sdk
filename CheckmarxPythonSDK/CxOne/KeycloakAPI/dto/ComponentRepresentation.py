from dataclasses import dataclass
from typing import Dict, List, Any, Optional
from typing_extensions import Self
from inflection import camelize, underscore


@dataclass
class ComponentRepresentation:
    id: Optional[str] = None
    name: Optional[str] = None
    provider_id: Optional[str] = None
    provider_type: Optional[str] = None
    parent_id: Optional[str] = None
    sub_type: Optional[str] = None
    config: Optional[Dict[str, Any]] = None

    def to_dict(self) -> Dict[str, Any]:
        result: Dict[str, Any] = {}
        if self.id is not None:
            value = self.id
            result['id'] = value
        if self.name is not None:
            value = self.name
            result['name'] = value
        if self.provider_id is not None:
            value = self.provider_id
            result['providerId'] = value
        if self.provider_type is not None:
            value = self.provider_type
            result['providerType'] = value
        if self.parent_id is not None:
            value = self.parent_id
            result['parentId'] = value
        if self.sub_type is not None:
            value = self.sub_type
            result['subType'] = value
        if self.config is not None:
            value = self.config
            result['config'] = value
        return result

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> Self:
        snake_data: Dict[str, Any] = {underscore(k): v for k, v in data.items()}

        required_fields = []
        missing = [f for f in required_fields if f not in snake_data]
        if missing:
            raise ValueError(f'missing required field: {missing}')
        return cls(**snake_data)
