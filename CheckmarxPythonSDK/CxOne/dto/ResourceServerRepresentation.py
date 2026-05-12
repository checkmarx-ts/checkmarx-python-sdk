from dataclasses import dataclass


@dataclass
class ResourceServerRepresentation:
    allow_remote_resource_management: ... = None
    client_id: ... = None
    decision_strategy: ... = None
    resource_server_representation_id: ... = None
    name: ... = None
    policies: ... = None
    policy_enforcement_mode: ... = None
    resources: ... = None
    scopes: ... = None

    @classmethod
    def from_dict(cls, item: dict) -> "ResourceServerRepresentation":
        return cls(
            allow_remote_resource_management=item.get("allowRemoteResourceManagement"),
            client_id=item.get("clientId"),
            decision_strategy=item.get("decisionStrategy"),
            resource_server_representation_id=item.get("id"),
            name=item.get("name"),
            policies=item.get("policies"),
            policy_enforcement_mode=item.get("policyEnforcementMode"),
            resources=item.get("resources"),
            scopes=item.get("scopes"),
        )
