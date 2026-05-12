from dataclasses import dataclass


@dataclass
class ScopeMappingRepresentation:
    client: ... = None
    client_scope: ... = None
    roles: ... = None
    scope_mapping_representation_self: ... = None

    @classmethod
    def from_dict(cls, item: dict) -> "ScopeMappingRepresentation":
        return cls(
            client=item.get("client"),
            client_scope=item.get("clientScope"),
            roles=item.get("roles"),
            scope_mapping_representation_self=item.get("self"),
        )
