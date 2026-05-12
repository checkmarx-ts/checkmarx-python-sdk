from dataclasses import dataclass


@dataclass
class ClientMappingsRepresentation:
    client: ... = None
    client_mappings_representation_id: ... = None
    mappings: ... = None

    @classmethod
    def from_dict(cls, item: dict) -> "ClientMappingsRepresentation":
        return cls(
            client=item.get("client"),
            client_mappings_representation_id=item.get("id"),
            mappings=item.get("mappings"),
        )
