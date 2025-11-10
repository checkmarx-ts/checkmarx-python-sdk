from dataclasses import dataclass
from typing import Dict, List, Any, Optional
from typing_extensions import Self
from inflection import camelize, underscore
from .UPAttribute import UPAttribute
from .UPGroup import UPGroup


@dataclass
class UPConfig:
    attributes: Optional[List[UPAttribute]] = None
    groups: Optional[List[UPGroup]] = None

    def to_dict(self) -> Dict[str, Any]:
        result: Dict[str, Any] = {}
        if self.attributes is not None:
            value = [item.to_dict() for item in self.attributes]
            result['attributes'] = value
        if self.groups is not None:
            value = [item.to_dict() for item in self.groups]
            result['groups'] = value
        return result

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> Self:
        snake_data: Dict[str, Any] = {underscore(k): v for k, v in data.items()}

        if 'attributes' in snake_data and snake_data['attributes'] is not None:
            snake_data['attributes'] = [
                UPAttribute.from_dict(item) for item in snake_data['attributes']
            ]
        if 'groups' in snake_data and snake_data['groups'] is not None:
            snake_data['groups'] = [
                UPGroup.from_dict(item) for item in snake_data['groups']
            ]
        required_fields = []
        missing = [f for f in required_fields if f not in snake_data]
        if missing:
            raise ValueError(f'missing required field: {missing}')
        return cls(**snake_data)
