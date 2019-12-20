

class AuthenticationProvider(object):

    def __init__(self, id, name, provider_id, provider_type, is_external, active):
        """

        Args:
            id:
            name:
            provider_id:
            provider_type:
            is_external:
            active:
        """
        self.id = id
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
