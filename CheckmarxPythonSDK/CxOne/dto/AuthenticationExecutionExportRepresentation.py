from dataclasses import dataclass


@dataclass
class AuthenticationExecutionExportRepresentation:
    authenticator: ... = None
    authenticator_config: ... = None
    authenticator_flow: ... = None
    flow_alias: ... = None
    priority: ... = None
    requirement: ... = None
    user_setup_allowed: ... = None

    @classmethod
    def from_dict(cls, item: dict) -> "AuthenticationExecutionExportRepresentation":
        return cls(
            authenticator=item.get("authenticator"),
            authenticator_config=item.get("authenticatorConfig"),
            authenticator_flow=item.get("authenticatorFlow"),
            flow_alias=item.get("flowAlias"),
            priority=item.get("priority"),
            requirement=item.get("requirement"),
            user_setup_allowed=item.get("userSetupAllowed"),
        )
