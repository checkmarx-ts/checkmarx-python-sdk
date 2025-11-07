class UserFederationMapperRepresentation:
    def __init__(self, config, federation_mapper_type, federation_provider_display_name,
                 user_federation_mapper_representation_id, name):
        self.config = config
        self.federationMapperType = federation_mapper_type
        self.federationProviderDisplayName = federation_provider_display_name
        self.id = user_federation_mapper_representation_id
        self.name = name

    def __str__(self):
        return f"UserFederationMapperRepresentation(" \
               f"config={self.config}, " \
               f"federationMapperType={self.federationMapperType}, " \
               f"federationProviderDisplayName={self.federationProviderDisplayName}, " \
               f"id={self.id}, " \
               f"name={self.name}" \
               f")"

    def to_dict(self):
        return {
            "config": self.config,
            "federationMapperType": self.federationMapperType,
            "federationProviderDisplayName": self.federationProviderDisplayName,
            "id": self.id,
            "name": self.name,
        }


def construct_user_federation_mapper_representation(item):
    return UserFederationMapperRepresentation(
        config=item.get("config"),
        federation_mapper_type=item.get("federationMapperType"),
        federation_provider_display_name=item.get("federationProviderDisplayName"),
        user_federation_mapper_representation_id=item.get("id"),
        name=item.get("name"),
    )
