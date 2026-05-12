from dataclasses import dataclass


@dataclass
class UserFederationMapperRepresentation:
    id: str
    name: str
    federation_provider_display_name: str
    federation_mapper_type: str
    config: dict
