from dataclasses import dataclass


@dataclass
class ProtocolMapperRepresentation:
    config: ... = None
    protocol_mapper_representation_id: ... = None
    name: ... = None
    protocol: ... = None
    protocol_mapper: ... = None

    @classmethod
    def from_dict(cls, item: dict) -> "ProtocolMapperRepresentation":
        return cls(
            config=item.get("config"),
            protocol_mapper_representation_id=item.get("id"),
            name=item.get("name"),
            protocol=item.get("protocol"),
            protocol_mapper=item.get("protocolMapper"),
        )
