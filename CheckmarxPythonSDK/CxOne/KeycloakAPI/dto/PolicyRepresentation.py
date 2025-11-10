from dataclasses import dataclass
from typing import Dict, List, Any, Optional
from typing_extensions import Self
from inflection import camelize, underscore
from .DecisionStrategy import DecisionStrategy
from .Logic import Logic
from .ResourceRepresentation import ResourceRepresentation
from .ScopeRepresentation import ScopeRepresentation


@dataclass
class PolicyRepresentation:
    id: Optional[str] = None
    name: Optional[str] = None
    description: Optional[str] = None
    type: Optional[str] = None
    policies: Optional[List[str]] = None
    resources: Optional[List[str]] = None
    scopes: Optional[List[str]] = None
    logic: Optional[Logic] = None
    decision_strategy: Optional[DecisionStrategy] = None
    owner: Optional[str] = None
    resources_data: Optional[List[ResourceRepresentation]] = None
    scopes_data: Optional[List[ScopeRepresentation]] = None
    config: Optional[Dict[str, Any]] = None

    def to_dict(self) -> Dict[str, Any]:
        result: Dict[str, Any] = {}
        if self.id is not None:
            value = self.id
            result['id'] = value
        if self.name is not None:
            value = self.name
            result['name'] = value
        if self.description is not None:
            value = self.description
            result['description'] = value
        if self.type is not None:
            value = self.type
            result['type'] = value
        if self.policies is not None:
            value = self.policies
            result['policies'] = value
        if self.resources is not None:
            value = self.resources
            result['resources'] = value
        if self.scopes is not None:
            value = self.scopes
            result['scopes'] = value
        if self.logic is not None:
            value = self.logic.to_dict()
            result['logic'] = value
        if self.decision_strategy is not None:
            value = self.decision_strategy.to_dict()
            result['decisionStrategy'] = value
        if self.owner is not None:
            value = self.owner
            result['owner'] = value
        if self.resources_data is not None:
            value = [item.to_dict() for item in self.resources_data]
            result['resourcesData'] = value
        if self.scopes_data is not None:
            value = [item.to_dict() for item in self.scopes_data]
            result['scopesData'] = value
        if self.config is not None:
            value = self.config
            result['config'] = value
        return result

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> Self:
        snake_data: Dict[str, Any] = {underscore(k): v for k, v in data.items()}

        if 'logic' in snake_data and snake_data['logic'] is not None:
            snake_data['logic'] = Logic.from_dict(snake_data['logic'])
        if 'decision_strategy' in snake_data and snake_data['decision_strategy'] is not None:
            snake_data['decision_strategy'] = DecisionStrategy.from_dict(snake_data['decision_strategy'])
        if 'resources_data' in snake_data and snake_data['resources_data'] is not None:
            snake_data['resources_data'] = [
                ResourceRepresentation.from_dict(item) for item in snake_data['resources_data']
            ]
        if 'scopes_data' in snake_data and snake_data['scopes_data'] is not None:
            snake_data['scopes_data'] = [
                ScopeRepresentation.from_dict(item) for item in snake_data['scopes_data']
            ]
        required_fields = []
        missing = [f for f in required_fields if f not in snake_data]
        if missing:
            raise ValueError(f'missing required field: {missing}')
        return cls(**snake_data)
