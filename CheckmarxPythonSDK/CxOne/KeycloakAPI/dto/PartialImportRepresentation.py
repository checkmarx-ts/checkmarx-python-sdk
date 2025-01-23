class PartialImportRepresentation:
    def __init__(self, clients, groups, identity_providers, if_resource_exists, policy, roles, users):
        self.clients = clients
        self.groups = groups
        self.identityProviders = identity_providers
        self.ifResourceExists = if_resource_exists
        self.policy = policy
        self.roles = roles
        self.users = users

    def __str__(self):
        return f"PartialImportRepresentation(" \
               f"clients={self.clients} " \
               f"groups={self.groups} " \
               f"identityProviders={self.identityProviders} " \
               f"ifResourceExists={self.ifResourceExists} " \
               f"policy={self.policy} " \
               f"roles={self.roles} " \
               f"users={self.users} " \
               f")"

    def to_dict(self):
        return {
            "clients": self.clients,
            "groups": self.groups,
            "identityProviders": self.identityProviders,
            "ifResourceExists": self.ifResourceExists,
            "policy": self.policy,
            "roles": self.roles,
            "users": self.users,
        }


def construct_partial_import_representation(item):
    return PartialImportRepresentation(
        clients=item.get("clients"),
        groups=item.get("groups"),
        identity_providers=item.get("identityProviders"),
        if_resource_exists=item.get("ifResourceExists"),
        policy=item.get("policy"),
        roles=item.get("roles"),
        users=item.get("users"),
    )
