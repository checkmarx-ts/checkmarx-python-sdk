class AuthenticationExecutionInfoRepresentation:
    def __init__(self, alias, authentication_config, authentication_flow, configurable, description, display_name,
                 flow_id, authentication_execution_info_representation_id, index, level, provider_id, requirement,
                 requirement_choices):
        self.alias = alias
        self.authenticationConfig = authentication_config
        self.authenticationFlow = authentication_flow
        self.configurable = configurable
        self.description = description
        self.displayName = display_name
        self.flowId = flow_id
        self.id = authentication_execution_info_representation_id
        self.index = index
        self.level = level
        self.providerId = provider_id
        self.requirement = requirement
        self.requirementChoices = requirement_choices

    def __str__(self):
        return f"AuthenticationExecutionInfoRepresentation(" \
               f"alias={self.alias} " \
               f"authenticationConfig={self.authenticationConfig} " \
               f"authenticationFlow={self.authenticationFlow} " \
               f"configurable={self.configurable} " \
               f"description={self.description} " \
               f"displayName={self.displayName} " \
               f"flowId={self.flowId} " \
               f"id={self.id} " \
               f"index={self.index} " \
               f"level={self.level} " \
               f"providerId={self.providerId} " \
               f"requirement={self.requirement} " \
               f"requirementChoices={self.requirementChoices} " \
               f")"

    def to_dict(self):
        return {
            "alias": self.alias,
            "authenticationConfig": self.authenticationConfig,
            "authenticationFlow": self.authenticationFlow,
            "configurable": self.configurable,
            "description": self.description,
            "displayName": self.displayName,
            "flowId": self.flowId,
            "id": self.id,
            "index": self.index,
            "level": self.level,
            "providerId": self.providerId,
            "requirement": self.requirement,
            "requirementChoices": self.requirementChoices,
        }


def construct_authentication_execution_info_representation(item):
    return AuthenticationExecutionInfoRepresentation(
        alias=item.get("alias"),
        authentication_config=item.get("authenticationConfig"),
        authentication_flow=item.get("authenticationFlow"),
        configurable=item.get("configurable"),
        description=item.get("description"),
        display_name=item.get("displayName"),
        flow_id=item.get("flowId"),
        authentication_execution_info_representation_id=item.get("id"),
        index=item.get("index"),
        level=item.get("level"),
        provider_id=item.get("providerId"),
        requirement=item.get("requirement"),
        requirement_choices=item.get("requirementChoices"),
    )
