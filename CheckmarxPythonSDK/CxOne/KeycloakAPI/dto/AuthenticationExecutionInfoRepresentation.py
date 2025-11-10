from dataclasses import dataclass
from typing import Dict, List, Any, Optional
from typing_extensions import Self
from inflection import camelize, underscore


@dataclass
class AuthenticationExecutionInfoRepresentation:
    id: Optional[str] = None
    requirement: Optional[str] = None
    display_name: Optional[str] = None
    alias: Optional[str] = None
    description: Optional[str] = None
    requirement_choices: Optional[List[str]] = None
    configurable: Optional[bool] = None
    authentication_flow: Optional[bool] = None
    provider_id: Optional[str] = None
    authentication_config: Optional[str] = None
    flow_id: Optional[str] = None
    level: Optional[int] = None
    index: Optional[int] = None

    def to_dict(self) -> Dict[str, Any]:
        result: Dict[str, Any] = {}
        if self.id is not None:
            value = self.id
            result['id'] = value
        if self.requirement is not None:
            value = self.requirement
            result['requirement'] = value
        if self.display_name is not None:
            value = self.display_name
            result['displayName'] = value
        if self.alias is not None:
            value = self.alias
            result['alias'] = value
        if self.description is not None:
            value = self.description
            result['description'] = value
        if self.requirement_choices is not None:
            value = self.requirement_choices
            result['requirementChoices'] = value
        if self.configurable is not None:
            value = self.configurable
            result['configurable'] = value
        if self.authentication_flow is not None:
            value = self.authentication_flow
            result['authenticationFlow'] = value
        if self.provider_id is not None:
            value = self.provider_id
            result['providerId'] = value
        if self.authentication_config is not None:
            value = self.authentication_config
            result['authenticationConfig'] = value
        if self.flow_id is not None:
            value = self.flow_id
            result['flowId'] = value
        if self.level is not None:
            value = self.level
            result['level'] = value
        if self.index is not None:
            value = self.index
            result['index'] = value
        return result

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> Self:
        snake_data: Dict[str, Any] = {underscore(k): v for k, v in data.items()}

        required_fields = []
        missing = [f for f in required_fields if f not in snake_data]
        if missing:
            raise ValueError(f'missing required field: {missing}')
        return cls(**snake_data)
