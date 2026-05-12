from dataclasses import dataclass


@dataclass
class ClientScopeRepresentation:
    attributes: ... = None
    description: ... = None
    client_scope_representation_id: ... = None
    name: ... = None
    protocol: ... = None
    protocol_mappers: ... = None

    @classmethod
    def from_dict(cls, item: dict) -> "ClientScopeRepresentation":
        return cls(
            attributes=item.get("attributes"),
            description=item.get("description"),
            client_scope_representation_id=item.get("id"),
            name=item.get("name"),
            protocol=item.get("protocol"),
            protocol_mappers=item.get("protocolMappers"),
        )
