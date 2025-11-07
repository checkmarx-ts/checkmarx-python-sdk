class PolicyRepresentation:
    def __init__(self, config, decision_strategy, description, policy_representation_id, logic, name, owner, policies,
                 resources, resources_data, scopes, scopes_data, policy_representation_type):
        self.config = config
        self.decisionStrategy = decision_strategy
        self.description = description
        self.id = policy_representation_id
        self.logic = logic
        self.name = name
        self.owner = owner
        self.policies = policies
        self.resources = resources
        self.resourcesData = resources_data
        self.scopes = scopes
        self.scopesData = scopes_data
        self.type = policy_representation_type

    def __str__(self):
        return f"PolicyRepresentation(" \
               f"config={self.config} " \
               f"decisionStrategy={self.decisionStrategy} " \
               f"description={self.description} " \
               f"id={self.id} " \
               f"logic={self.logic} " \
               f"name={self.name} " \
               f"owner={self.owner} " \
               f"policies={self.policies} " \
               f"resources={self.resources} " \
               f"resourcesData={self.resourcesData} " \
               f"scopes={self.scopes} " \
               f"scopesData={self.scopesData} " \
               f"type={self.type} " \
               f")"

    def to_dict(self):
        return {
            "config": self.config,
            "decisionStrategy": self.decisionStrategy,
            "description": self.description,
            "id": self.id,
            "logic": self.logic,
            "name": self.name,
            "owner": self.owner,
            "policies": self.policies,
            "resources": self.resources,
            "resourcesData": self.resourcesData,
            "scopes": self.scopes,
            "scopesData": self.scopesData,
            "type": self.type,
        }


def construct_policy_representation(item):
    return PolicyRepresentation(
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
