class ScopeMappingRepresentation:
    def __init__(self, client, client_scope, roles, scope_mapping_representation_self):
        self.client = client
        self.clientScope = client_scope
        self.roles = roles
        self.self = scope_mapping_representation_self

    def __str__(self):
        return f"ScopeMappingRepresentation(" \
               f"client={self.client} " \
               f"clientScope={self.clientScope} " \
               f"roles={self.roles} " \
               f"self={self.self} " \
               f")"

    def to_dict(self):
        return {
            "client": self.client,
            "clientScope": self.clientScope,
            "roles": self.roles,
            "self": self.self,
        }


def construct_scope_mapping_representation(item):
    return ScopeMappingRepresentation(
        client=item.get("client"),
        client_scope=item.get("clientScope"),
        roles=item.get("roles"),
        scope_mapping_representation_self=item.get("self"),
    )
