class AuthenticationExecutionExportRepresentation:
    def __init__(self, authenticator, authenticator_config, authenticator_flow, flow_alias, priority, requirement,
                 user_setup_allowed):
        self.authenticator = authenticator
        self.authenticatorConfig = authenticator_config
        self.authenticatorFlow = authenticator_flow
        self.flowAlias = flow_alias
        self.priority = priority
        self.requirement = requirement
        self.userSetupAllowed = user_setup_allowed

    def __str__(self):
        return f"AuthenticationExecutionExportRepresentation(" \
               f"authenticator={self.authenticator} " \
               f"authenticatorConfig={self.authenticatorConfig} " \
               f"authenticatorFlow={self.authenticatorFlow} " \
               f"flowAlias={self.flowAlias} " \
               f"priority={self.priority} " \
               f"requirement={self.requirement} " \
               f"userSetupAllowed={self.userSetupAllowed} " \
               f")"

    def to_dict(self):
        return {
            "authenticator": self.authenticator,
            "authenticatorConfig": self.authenticatorConfig,
            "authenticatorFlow": self.authenticatorFlow,
            "flowAlias": self.flowAlias,
            "priority": self.priority,
            "requirement": self.requirement,
            "userSetupAllowed": self.userSetupAllowed,
        }


def construct_authentication_execution_export_representation(item):
    return AuthenticationExecutionExportRepresentation(
        authenticator=item.get("authenticator"),
        authenticator_config=item.get("authenticatorConfig"),
        authenticator_flow=item.get("authenticatorFlow"),
        flow_alias=item.get("flowAlias"),
        priority=item.get("priority"),
        requirement=item.get("requirement"),
        user_setup_allowed=item.get("userSetupAllowed"),
    )
