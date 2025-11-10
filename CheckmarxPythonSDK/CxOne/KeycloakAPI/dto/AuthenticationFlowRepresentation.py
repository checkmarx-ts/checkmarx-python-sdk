from dataclasses import dataclass
from typing import Dict, List, Any, Optional
from typing_extensions import Self
from inflection import camelize, underscore
from .AuthenticationExecutionExportRepresentation import AuthenticationExecutionExportRepresentation


@dataclass
class AuthenticationFlowRepresentation:
    id: Optional[str] = None
    alias: Optional[str] = None
    description: Optional[str] = None
    provider_id: Optional[str] = None
    top_level: Optional[bool] = None
    built_in: Optional[bool] = None
    authentication_executions: Optional[List[AuthenticationExecutionExportRepresentation]] = None

    def to_dict(self) -> Dict[str, Any]:
        result: Dict[str, Any] = {}
        if self.id is not None:
            value = self.id
            result['id'] = value
        if self.alias is not None:
            value = self.alias
            result['alias'] = value
        if self.description is not None:
            value = self.description
            result['description'] = value
        if self.provider_id is not None:
            value = self.provider_id
            result['providerId'] = value
        if self.top_level is not None:
            value = self.top_level
            result['topLevel'] = value
        if self.built_in is not None:
            value = self.built_in
            result['builtIn'] = value
        if self.authentication_executions is not None:
            value = [item.to_dict() for item in self.authentication_executions]
            result['authenticationExecutions'] = value
        return result

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> Self:
        snake_data: Dict[str, Any] = {underscore(k): v for k, v in data.items()}

        if 'authentication_executions' in snake_data and snake_data['authentication_executions'] is not None:
            snake_data['authentication_executions'] = [
                AuthenticationExecutionExportRepresentation.from_dict(item) for item in
                snake_data['authentication_executions']
            ]
        required_fields = []
        missing = [f for f in required_fields if f not in snake_data]
        if missing:
            raise ValueError(f'missing required field: {missing}')
        return cls(**snake_data)
