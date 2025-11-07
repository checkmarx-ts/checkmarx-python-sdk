class AuthenticationFlowRepresentation:
    def __init__(self, alias, authentication_executions, built_in, description, authentication_flow_representation_id,
                 provider_id, top_level):
        self.alias = alias
        self.authenticationExecutions = authentication_executions
        self.builtIn = built_in
        self.description = description
        self.id = authentication_flow_representation_id
        self.providerId = provider_id
        self.topLevel = top_level

    def __str__(self):
        return f"AuthenticationFlowRepresentation(" \
               f"alias={self.alias} " \
               f"authenticationExecutions={self.authenticationExecutions} " \
               f"builtIn={self.builtIn} " \
               f"description={self.description} " \
               f"id={self.id} " \
               f"providerId={self.providerId} " \
               f"topLevel={self.topLevel} " \
               f")"

    def to_dict(self):
        return {
            "alias": self.alias,
            "authenticationExecutions": self.authenticationExecutions,
            "builtIn": self.builtIn,
            "description": self.description,
            "id": self.id,
            "providerId": self.providerId,
            "topLevel": self.topLevel,
        }


def construct_authentication_flow_representation(item):
    return AuthenticationFlowRepresentation(
        alias=item.get("alias"),
        authentication_executions=item.get("authenticationExecutions"),
        built_in=item.get("builtIn"),
        description=item.get("description"),
        authentication_flow_representation_id=item.get("id"),
        provider_id=item.get("providerId"),
        top_level=item.get("topLevel"),
    )
