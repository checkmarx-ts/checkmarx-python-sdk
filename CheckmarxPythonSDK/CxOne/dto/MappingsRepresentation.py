from dataclasses import dataclass


@dataclass
class MappingsRepresentation:
    client_mappings: ... = None
    realm_mappings: ... = None

    @classmethod
    def from_dict(cls, item: dict) -> "MappingsRepresentation":
        return cls(
            client_mappings=item.get("clientMappings"),
            realm_mappings=item.get("realmMappings"),
        )
