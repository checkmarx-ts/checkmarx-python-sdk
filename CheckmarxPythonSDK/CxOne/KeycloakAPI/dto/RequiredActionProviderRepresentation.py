from dataclasses import dataclass
from typing import Dict, List, Any, Optional
from typing_extensions import Self
from inflection import camelize, underscore


@dataclass
class RequiredActionProviderRepresentation:
    alias: Optional[str] = None
    name: Optional[str] = None
    provider_id: Optional[str] = None
    enabled: Optional[bool] = None
    default_action: Optional[bool] = None
    priority: Optional[int] = None
    config: Optional[Dict[str, Any]] = None

    def to_dict(self) -> Dict[str, Any]:
        result: Dict[str, Any] = {}
        if self.alias is not None:
            value = self.alias
            result['alias'] = value
        if self.name is not None:
            value = self.name
            result['name'] = value
        if self.provider_id is not None:
            value = self.provider_id
            result['providerId'] = value
        if self.enabled is not None:
            value = self.enabled
            result['enabled'] = value
        if self.default_action is not None:
            value = self.default_action
            result['defaultAction'] = value
        if self.priority is not None:
            value = self.priority
            result['priority'] = value
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
