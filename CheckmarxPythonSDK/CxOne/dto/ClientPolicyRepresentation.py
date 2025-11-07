class ClientPolicyRepresentation:
    def __init__(self, conditions, description, enabled, name, profiles):
        self.conditions = conditions
        self.description = description
        self.enabled = enabled
        self.name = name
        self.profiles = profiles

    def __str__(self):
        return f"ClientPolicyRepresentation(" \
               f"conditions={self.conditions} " \
               f"description={self.description} " \
               f"enabled={self.enabled} " \
               f"name={self.name} " \
               f"profiles={self.profiles} " \
               f")"

    def to_dict(self):
        return {
            "conditions": self.conditions,
            "description": self.description,
            "enabled": self.enabled,
            "name": self.name,
            "profiles": self.profiles,
        }


def construct_client_policy_representation(item):
    return ClientPolicyRepresentation(
        conditions=item.get("conditions"),
        description=item.get("description"),
        enabled=item.get("enabled"),
        name=item.get("name"),
        profiles=item.get("profiles"),
    )
