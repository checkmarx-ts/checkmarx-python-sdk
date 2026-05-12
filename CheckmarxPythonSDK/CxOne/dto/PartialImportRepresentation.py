from dataclasses import dataclass


@dataclass
class PartialImportRepresentation:
    clients: ... = None
    groups: ... = None
    identity_providers: ... = None
    if_resource_exists: ... = None
    policy: ... = None
    roles: ... = None
    users: ... = None

    @classmethod
    def from_dict(cls, item: dict) -> "PartialImportRepresentation":
        return cls(
            clients=item.get("clients"),
            groups=item.get("groups"),
            identity_providers=item.get("identityProviders"),
            if_resource_exists=item.get("ifResourceExists"),
            policy=item.get("policy"),
            roles=item.get("roles"),
            users=item.get("users"),
        )
