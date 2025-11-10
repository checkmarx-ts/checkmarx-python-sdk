from dataclasses import dataclass
from typing import Dict, List, Any, Optional
from typing_extensions import Self
from inflection import camelize, underscore
from .DecisionStrategy import DecisionStrategy
from .PolicyEnforcementMode import PolicyEnforcementMode
from .PolicyRepresentation import PolicyRepresentation
from .ResourceRepresentation import ResourceRepresentation
from .ScopeRepresentation import ScopeRepresentation


@dataclass
class ResourceServerRepresentation:
    id: Optional[str] = None
    client_id: Optional[str] = None
    name: Optional[str] = None
    allow_remote_resource_management: Optional[bool] = None
    policy_enforcement_mode: Optional[PolicyEnforcementMode] = None
    resources: Optional[List[ResourceRepresentation]] = None
    policies: Optional[List[PolicyRepresentation]] = None
    scopes: Optional[List[ScopeRepresentation]] = None
    decision_strategy: Optional[DecisionStrategy] = None

    def to_dict(self) -> Dict[str, Any]:
        result: Dict[str, Any] = {}
        if self.id is not None:
            value = self.id
            result['id'] = value
        if self.client_id is not None:
            value = self.client_id
            result['clientId'] = value
        if self.name is not None:
            value = self.name
            result['name'] = value
        if self.allow_remote_resource_management is not None:
            value = self.allow_remote_resource_management
            result['allowRemoteResourceManagement'] = value
        if self.policy_enforcement_mode is not None:
            value = self.policy_enforcement_mode.to_dict()
            result['policyEnforcementMode'] = value
        if self.resources is not None:
            value = [item.to_dict() for item in self.resources]
            result['resources'] = value
        if self.policies is not None:
            value = [item.to_dict() for item in self.policies]
            result['policies'] = value
        if self.scopes is not None:
            value = [item.to_dict() for item in self.scopes]
            result['scopes'] = value
        if self.decision_strategy is not None:
            value = self.decision_strategy.to_dict()
            result['decisionStrategy'] = value
        return result

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> Self:
        snake_data: Dict[str, Any] = {underscore(k): v for k, v in data.items()}

        if 'policy_enforcement_mode' in snake_data and snake_data['policy_enforcement_mode'] is not None:
            snake_data['policy_enforcement_mode'] = PolicyEnforcementMode.from_dict(
                snake_data['policy_enforcement_mode'])
        if 'decision_strategy' in snake_data and snake_data['decision_strategy'] is not None:
            snake_data['decision_strategy'] = DecisionStrategy.from_dict(snake_data['decision_strategy'])
        if 'resources' in snake_data and snake_data['resources'] is not None:
            snake_data['resources'] = [
                ResourceRepresentation.from_dict(item) for item in snake_data['resources']
            ]
        if 'policies' in snake_data and snake_data['policies'] is not None:
            snake_data['policies'] = [
                PolicyRepresentation.from_dict(item) for item in snake_data['policies']
            ]
        if 'scopes' in snake_data and snake_data['scopes'] is not None:
            snake_data['scopes'] = [
                ScopeRepresentation.from_dict(item) for item in snake_data['scopes']
            ]
        required_fields = []
        missing = [f for f in required_fields if f not in snake_data]
        if missing:
            raise ValueError(f'missing required field: {missing}')
        return cls(**snake_data)
