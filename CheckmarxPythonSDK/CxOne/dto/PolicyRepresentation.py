from dataclasses import dataclass


@dataclass
class PolicyRepresentation:
    config: ... = None
    decision_strategy: ... = None
    description: ... = None
    policy_representation_id: ... = None
    logic: ... = None
    name: ... = None
    owner: ... = None
    policies: ... = None
    resources: ... = None
    resources_data: ... = None
    scopes: ... = None
    scopes_data: ... = None
    policy_representation_type: ... = None

    @classmethod
    def from_dict(cls, item: dict) -> "PolicyRepresentation":
        return cls(
            config=item.get("config"),
            decision_strategy=item.get("decisionStrategy"),
            description=item.get("description"),
            policy_representation_id=item.get("id"),
            logic=item.get("logic"),
            name=item.get("name"),
            owner=item.get("owner"),
            policies=item.get("policies"),
            resources=item.get("resources"),
            resources_data=item.get("resourcesData"),
            scopes=item.get("scopes"),
            scopes_data=item.get("scopesData"),
            policy_representation_type=item.get("type"),
        )
