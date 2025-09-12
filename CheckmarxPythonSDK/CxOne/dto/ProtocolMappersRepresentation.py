from dataclasses import dataclass


@dataclass
class ProtocolMappersRepresentation:
    id: str = None
    name: str = None
    protocol: str = None
    protocol_mapper: str = None
    consent_required: bool = None
    config: str = None


def construct_protocol_mappers_representation(item):
    return ProtocolMappersRepresentation(
        id=item.get("id"),
        name=item.get("name"),
        protocol=item.get("protocol"),
        protocol_mapper=item.get("protocolMapper"),
        consent_required=item.get("consentRequired"),
        config=item.get("config")
    )
