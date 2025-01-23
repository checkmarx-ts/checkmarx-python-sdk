class IdentityProviderMapperRepresentation:
    def __init__(self, config, identity_provider_mapper_representation_id, identity_provider_alias,
                 identity_provider_mapper, name):
        self.config = config
        self.id = identity_provider_mapper_representation_id
        self.identityProviderAlias = identity_provider_alias
        self.identityProviderMapper = identity_provider_mapper
        self.name = name

    def __str__(self):
        return f"IdentityProviderMapperRepresentation(" \
               f"config={self.config} " \
               f"id={self.id} " \
               f"identityProviderAlias={self.identityProviderAlias} " \
               f"identityProviderMapper={self.identityProviderMapper} " \
               f"name={self.name} " \
               f")"

    def to_dict(self):
        return {
            "config": self.config,
            "id": self.id,
            "identityProviderAlias": self.identityProviderAlias,
            "identityProviderMapper": self.identityProviderMapper,
            "name": self.name,
        }


def construct_identity_provider_mapper_representation(item):
    return IdentityProviderMapperRepresentation(
        config=item.get("config"),
        identity_provider_mapper_representation_id=item.get("id"),
        identity_provider_alias=item.get("identityProviderAlias"),
        identity_provider_mapper=item.get("identityProviderMapper"),
        name=item.get("name"),
    )
