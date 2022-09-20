# encoding: utf-8


class AuthenticationProvider(object):

    def __init__(self, authentication_provider_id, name, provider_id, provider_type, is_external, active):
        """

        Args:
            authentication_provider_id (int):
            name (str):
            provider_id (int):
            provider_type (str):
            is_external (bool):
            active (bool):
        """
        self.id = authentication_provider_id
        self.name = name
        self.provider_id = provider_id
        self.provider_type = provider_type
        self.is_external = is_external
        self.active = active

    def __str__(self):
        return """AuthenticationProvider(id={}, name={}, provider_id={}, 
        provider_type={}, is_external={}, active={})""".format(
            self.id, self.name, self.provider_id, self.provider_type, self.is_external, self.active
        )
