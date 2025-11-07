class AuthenticatorConfigInfoRepresentation:
    def __init__(self, help_text, name, properties, provider_id):
        self.helpText = help_text
        self.name = name
        self.properties = properties
        self.providerId = provider_id

    def __str__(self):
        return f"AuthenticatorConfigInfoRepresentation(" \
               f"helpText={self.helpText} " \
               f"name={self.name} " \
               f"properties={self.properties} " \
               f"providerId={self.providerId} " \
               f")"

    def to_dict(self):
        return {
            "helpText": self.helpText,
            "name": self.name,
            "properties": self.properties,
            "providerId": self.providerId,
        }


def construct_authenticator_config_info_representation(item):
    return AuthenticatorConfigInfoRepresentation(
        help_text=item.get("helpText"),
        name=item.get("name"),
        properties=item.get("properties"),
        provider_id=item.get("providerId"),
    )
