class ResourceServerRepresentation:
    def __init__(self, allow_remote_resource_management, client_id, decision_strategy,
                 resource_server_representation_id, name, policies, policy_enforcement_mode, resources, scopes):
        self.allowRemoteResourceManagement = allow_remote_resource_management
        self.clientId = client_id
        self.decisionStrategy = decision_strategy
        self.id = resource_server_representation_id
        self.name = name
        self.policies = policies
        self.policyEnforcementMode = policy_enforcement_mode
        self.resources = resources
        self.scopes = scopes

    def __str__(self):
        return f"ResourceServerRepresentation(" \
               f"allowRemoteResourceManagement={self.allowRemoteResourceManagement} " \
               f"clientId={self.clientId} " \
               f"decisionStrategy={self.decisionStrategy} " \
               f"id={self.id} " \
               f"name={self.name} " \
               f"policies={self.policies} " \
               f"policyEnforcementMode={self.policyEnforcementMode} " \
               f"resources={self.resources} " \
               f"scopes={self.scopes} " \
               f")"

    def to_dict(self):
        return {
            "allowRemoteResourceManagement": self.allowRemoteResourceManagement,
            "clientId": self.clientId,
            "decisionStrategy": self.decisionStrategy,
            "id": self.id,
            "name": self.name,
            "policies": self.policies,
            "policyEnforcementMode": self.policyEnforcementMode,
            "resources": self.resources,
            "scopes": self.scopes,
        }


def construct_resource_server_representation(item):
    return ResourceServerRepresentation(
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
