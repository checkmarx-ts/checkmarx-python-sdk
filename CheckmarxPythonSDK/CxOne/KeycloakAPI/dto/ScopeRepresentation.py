class ScopeRepresentation:
    def __init__(self, display_name, icon_uri, scope_representation_id, name, policies, resources):
        self.displayName = display_name
        self.iconUri = icon_uri
        self.id = scope_representation_id
        self.name = name
        self.policies = policies
        self.resources = resources

    def __str__(self):
        return f"ScopeRepresentation(" \
               f"displayName={self.displayName} " \
               f"iconUri={self.iconUri} " \
               f"id={self.id} " \
               f"name={self.name} " \
               f"policies={self.policies} " \
               f"resources={self.resources} " \
               f")"

    def to_dict(self):
        return {
            "displayName": self.displayName,
            "iconUri": self.iconUri,
            "id": self.id,
            "name": self.name,
            "policies": self.policies,
            "resources": self.resources,
        }


def construct_scope_representation(item):
    return ScopeRepresentation(
        display_name=item.get("displayName"),
        icon_uri=item.get("iconUri"),
        scope_representation_id=item.get("id"),
        name=item.get("name"),
        policies=item.get("policies"),
        resources=item.get("resources"),
    )
