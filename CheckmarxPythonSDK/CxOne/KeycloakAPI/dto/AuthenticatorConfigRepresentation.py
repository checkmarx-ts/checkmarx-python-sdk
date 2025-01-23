class AuthenticatorConfigRepresentation:
    def __init__(self, alias, config, authenticator_config_representation_id):
        self.alias = alias
        self.config = config
        self.id = authenticator_config_representation_id

    def __str__(self):
        return f"AuthenticatorConfigRepresentation(" \
               f"alias={self.alias} " \
               f"config={self.config} " \
               f"id={self.id} " \
               f")"

    def to_dict(self):
        return {
            "alias": self.alias,
            "config": self.config,
            "id": self.id,
        }


def construct_authenticator_config_representation(item):
    return AuthenticatorConfigRepresentation(
        alias=item.get("alias"),
        config=item.get("config"),
        authenticator_config_representation_id=item.get("id"),
    )
