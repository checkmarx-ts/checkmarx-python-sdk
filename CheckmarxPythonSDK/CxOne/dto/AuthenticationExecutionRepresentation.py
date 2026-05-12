from dataclasses import dataclass


@dataclass
class AuthenticationExecutionRepresentation:
    authenticator: ... = None
    authenticator_config: ... = None
    authenticator_flow: ... = None
    flow_id: ... = None
    authentication_execution_representation_id: ... = None
    parent_flow: ... = None
    priority: ... = None
    requirement: ... = None

    @classmethod
    def from_dict(cls, item: dict) -> "AuthenticationExecutionRepresentation":
        return cls(
            authenticator=item.get("authenticator"),
            authenticator_config=item.get("authenticatorConfig"),
            authenticator_flow=item.get("authenticatorFlow"),
            flow_id=item.get("flowId"),
            authentication_execution_representation_id=item.get("id"),
            parent_flow=item.get("parentFlow"),
            priority=item.get("priority"),
            requirement=item.get("requirement"),
        )
