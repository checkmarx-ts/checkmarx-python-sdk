from dataclasses import dataclass


@dataclass
class ProtocolMappersRepresentation:
    id: str = None
    name: str = None
    protocol: str = None
    protocol_mapper: str = None
    consent_required: bool = None
    config: str = None

    @classmethod
    def from_dict(cls, item: dict) -> "ProtocolMappersRepresentation":
        return cls(
            id=item.get("id"),
            name=item.get("name"),
            protocol=item.get("protocol"),
            protocol_mapper=item.get("protocolMapper"),
            consent_required=item.get("consentRequired"),
            config=item.get("config"),
        )
