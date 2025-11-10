from dataclasses import dataclass
from typing import Dict, List, Any, Optional
from typing_extensions import Self
from inflection import camelize, underscore
from .Permission import Permission


@dataclass
class Authorization:
    permissions: Optional[List[Permission]] = None

    def to_dict(self) -> Dict[str, Any]:
        result: Dict[str, Any] = {}
        if self.permissions is not None:
            value = [item.to_dict() for item in self.permissions]
            result['permissions'] = value
        return result

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> Self:
        snake_data: Dict[str, Any] = {underscore(k): v for k, v in data.items()}

        if 'permissions' in snake_data and snake_data['permissions'] is not None:
            snake_data['permissions'] = [
                Permission.from_dict(item) for item in snake_data['permissions']
            ]
        required_fields = []
        missing = [f for f in required_fields if f not in snake_data]
        if missing:
            raise ValueError(f'missing required field: {missing}')
        return cls(**snake_data)
