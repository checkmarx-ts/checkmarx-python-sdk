from dataclasses import dataclass
from typing import Dict, List, Any, Optional
from typing_extensions import Self
from inflection import camelize, underscore


@dataclass
class ScopeMappingRepresentation:
    self: Optional[str] = None
    client: Optional[str] = None
    client_template: Optional[str] = None
    client_scope: Optional[str] = None
    roles: Optional[List[str]] = None

    def to_dict(self) -> Dict[str, Any]:
        result: Dict[str, Any] = {}
        if self.self is not None:
            value = self.self
            result['self'] = value
        if self.client is not None:
            value = self.client
            result['client'] = value
        if self.client_template is not None:
            value = self.client_template
            result['clientTemplate'] = value
        if self.client_scope is not None:
            value = self.client_scope
            result['clientScope'] = value
        if self.roles is not None:
            value = self.roles
            result['roles'] = value
        return result

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> Self:
        snake_data: Dict[str, Any] = {underscore(k): v for k, v in data.items()}

        required_fields = []
        missing = [f for f in required_fields if f not in snake_data]
        if missing:
            raise ValueError(f'missing required field: {missing}')
        return cls(**snake_data)
