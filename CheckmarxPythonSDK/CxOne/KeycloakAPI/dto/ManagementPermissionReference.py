from dataclasses import dataclass
from typing import Dict, List, Any, Optional
from typing_extensions import Self
from inflection import camelize, underscore


@dataclass
class ManagementPermissionReference:
    enabled: Optional[bool] = None
    resource: Optional[str] = None
    scope_permissions: Optional[Dict[str, Any]] = None

    def to_dict(self) -> Dict[str, Any]:
        result: Dict[str, Any] = {}
        if self.enabled is not None:
            value = self.enabled
            result['enabled'] = value
        if self.resource is not None:
            value = self.resource
            result['resource'] = value
        if self.scope_permissions is not None:
            value = self.scope_permissions
            result['scopePermissions'] = value
        return result

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> Self:
        snake_data: Dict[str, Any] = {underscore(k): v for k, v in data.items()}

        required_fields = []
        missing = [f for f in required_fields if f not in snake_data]
        if missing:
            raise ValueError(f'missing required field: {missing}')
        return cls(**snake_data)
