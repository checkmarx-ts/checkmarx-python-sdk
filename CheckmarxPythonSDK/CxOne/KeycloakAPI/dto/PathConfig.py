from dataclasses import dataclass
from typing import Dict, List, Any, Optional
from typing_extensions import Self
from inflection import camelize, underscore
from .EnforcementMode import EnforcementMode
from .MethodConfig import MethodConfig


@dataclass
class PathConfig:
    name: Optional[str] = None
    type: Optional[str] = None
    path: Optional[str] = None
    methods: Optional[List[MethodConfig]] = None
    scopes: Optional[List[str]] = None
    id: Optional[str] = None
    enforcement_mode: Optional[EnforcementMode] = None
    claim_information_point: Optional[Dict[str, Any]] = None
    invalidated: Optional[bool] = None
    static_path: Optional[bool] = None
    static: Optional[bool] = None

    def to_dict(self) -> Dict[str, Any]:
        result: Dict[str, Any] = {}
        if self.name is not None:
            value = self.name
            result['name'] = value
        if self.type is not None:
            value = self.type
            result['type'] = value
        if self.path is not None:
            value = self.path
            result['path'] = value
        if self.methods is not None:
            value = [item.to_dict() for item in self.methods]
            result['methods'] = value
        if self.scopes is not None:
            value = self.scopes
            result['scopes'] = value
        if self.id is not None:
            value = self.id
            result['id'] = value
        if self.enforcement_mode is not None:
            value = self.enforcement_mode.to_dict()
            result['enforcementMode'] = value
        if self.claim_information_point is not None:
            value = self.claim_information_point
            result['claimInformationPoint'] = value
        if self.invalidated is not None:
            value = self.invalidated
            result['invalidated'] = value
        if self.static_path is not None:
            value = self.static_path
            result['staticPath'] = value
        if self.static is not None:
            value = self.static
            result['static'] = value
        return result

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> Self:
        snake_data: Dict[str, Any] = {underscore(k): v for k, v in data.items()}

        if 'enforcement_mode' in snake_data and snake_data['enforcement_mode'] is not None:
            snake_data['enforcement_mode'] = EnforcementMode.from_dict(snake_data['enforcement_mode'])
        if 'methods' in snake_data and snake_data['methods'] is not None:
            snake_data['methods'] = [
                MethodConfig.from_dict(item) for item in snake_data['methods']
            ]
        required_fields = []
        missing = [f for f in required_fields if f not in snake_data]
        if missing:
            raise ValueError(f'missing required field: {missing}')
        return cls(**snake_data)
