from dataclasses import dataclass


@dataclass
class UserFederationMapperRepresentation:
    id: str
    name: str
    federation_provider_display_name: str
    federation_mapper_type: str
    config: dict

    def to_dict(self):
        return {
            "id": self.id,
            "name": self.name,
            "federationProviderDisplayName": self.federation_provider_display_name,
            "federationMapperType": self.federation_mapper_type,
            "config": self.config,
        }


def construct_user_federation_mapper_representation(item):
    return UserFederationMapperRepresentation(
        id=item.get("id"),
        name=item.get("name"),
        federation_provider_display_name=item.get("federationProviderDisplayName"),
        federation_mapper_type=item.get("federationMapperType"),
        config=item.get("config"),
    )
