class AuthenticationExecutionRepresentation:
    def __init__(self, authenticator, authenticator_config, authenticator_flow, flow_id,
                 authentication_execution_representation_id, parent_flow, priority, requirement):
        self.authenticator = authenticator
        self.authenticatorConfig = authenticator_config
        self.authenticatorFlow = authenticator_flow
        self.flowId = flow_id
        self.id = authentication_execution_representation_id
        self.parentFlow = parent_flow
        self.priority = priority
        self.requirement = requirement

    def __str__(self):
        return f"AuthenticationExecutionRepresentation(" \
               f"authenticator={self.authenticator} " \
               f"authenticatorConfig={self.authenticatorConfig} " \
               f"authenticatorFlow={self.authenticatorFlow} " \
               f"flowId={self.flowId} " \
               f"id={self.id} " \
               f"parentFlow={self.parentFlow} " \
               f"priority={self.priority} " \
               f"requirement={self.requirement} " \
               f")"

    def to_dict(self):
        return {
            "authenticator": self.authenticator,
            "authenticatorConfig": self.authenticatorConfig,
            "authenticatorFlow": self.authenticatorFlow,
            "flowId": self.flowId,
            "id": self.id,
            "parentFlow": self.parentFlow,
            "priority": self.priority,
            "requirement": self.requirement,
        }


def construct_authentication_execution_representation(item):
    return AuthenticationExecutionRepresentation(
        authenticator=item.get("authenticator"),
        authenticator_config=item.get("authenticatorConfig"),
        authenticator_flow=item.get("authenticatorFlow"),
        flow_id=item.get("flowId"),
        authentication_execution_representation_id=item.get("id"),
        parent_flow=item.get("parentFlow"),
        priority=item.get("priority"),
        requirement=item.get("requirement"),
    )
