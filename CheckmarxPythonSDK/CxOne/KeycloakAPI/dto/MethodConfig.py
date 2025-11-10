from dataclasses import dataclass
from typing import Dict, List, Any, Optional
from typing_extensions import Self
from inflection import camelize, underscore
from .ScopeEnforcementMode import ScopeEnforcementMode


@dataclass
class MethodConfig:
    method: Optional[str] = None
    scopes: Optional[List[str]] = None
    scopes_enforcement_mode: Optional[ScopeEnforcementMode] = None

    def to_dict(self) -> Dict[str, Any]:
        result: Dict[str, Any] = {}
        if self.method is not None:
            value = self.method
            result['method'] = value
        if self.scopes is not None:
            value = self.scopes
            result['scopes'] = value
        if self.scopes_enforcement_mode is not None:
            value = self.scopes_enforcement_mode.to_dict()
            result['scopesEnforcementMode'] = value
        return result

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> Self:
        snake_data: Dict[str, Any] = {underscore(k): v for k, v in data.items()}

        if 'scopes_enforcement_mode' in snake_data and snake_data['scopes_enforcement_mode'] is not None:
            snake_data['scopes_enforcement_mode'] = ScopeEnforcementMode.from_dict(
                snake_data['scopes_enforcement_mode'])
        required_fields = []
        missing = [f for f in required_fields if f not in snake_data]
        if missing:
            raise ValueError(f'missing required field: {missing}')
        return cls(**snake_data)
