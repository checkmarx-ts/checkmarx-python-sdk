from dataclasses import dataclass


@dataclass
class IdentityProviderMapperRepresentation:
    config: ... = None
    identity_provider_mapper_representation_id: ... = None
    identity_provider_alias: ... = None
    identity_provider_mapper: ... = None
    name: ... = None

    @classmethod
    def from_dict(cls, item: dict) -> "IdentityProviderMapperRepresentation":
        return cls(
            config=item.get("config"),
            identity_provider_mapper_representation_id=item.get("id"),
            identity_provider_alias=item.get("identityProviderAlias"),
            identity_provider_mapper=item.get("identityProviderMapper"),
            name=item.get("name"),
        )
