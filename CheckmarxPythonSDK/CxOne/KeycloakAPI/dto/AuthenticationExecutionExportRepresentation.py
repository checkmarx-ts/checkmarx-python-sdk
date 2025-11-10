from dataclasses import dataclass
from typing import Dict, List, Any, Optional
from typing_extensions import Self
from inflection import camelize, underscore


@dataclass
class AuthenticationExecutionExportRepresentation:
    authenticator_config: Optional[str] = None
    authenticator: Optional[str] = None
    authenticator_flow: Optional[bool] = None
    requirement: Optional[str] = None
    priority: Optional[int] = None
    autheticator_flow: Optional[bool] = None
    flow_alias: Optional[str] = None
    user_setup_allowed: Optional[bool] = None

    def to_dict(self) -> Dict[str, Any]:
        result: Dict[str, Any] = {}
        if self.authenticator_config is not None:
            value = self.authenticator_config
            result['authenticatorConfig'] = value
        if self.authenticator is not None:
            value = self.authenticator
            result['authenticator'] = value
        if self.authenticator_flow is not None:
            value = self.authenticator_flow
            result['authenticatorFlow'] = value
        if self.requirement is not None:
            value = self.requirement
            result['requirement'] = value
        if self.priority is not None:
            value = self.priority
            result['priority'] = value
        if self.autheticator_flow is not None:
            value = self.autheticator_flow
            result['autheticatorFlow'] = value
        if self.flow_alias is not None:
            value = self.flow_alias
            result['flowAlias'] = value
        if self.user_setup_allowed is not None:
            value = self.user_setup_allowed
            result['userSetupAllowed'] = value
        return result

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> Self:
        snake_data: Dict[str, Any] = {underscore(k): v for k, v in data.items()}

        required_fields = []
        missing = [f for f in required_fields if f not in snake_data]
        if missing:
            raise ValueError(f'missing required field: {missing}')
        return cls(**snake_data)
