from dataclasses import dataclass


@dataclass
class AuthenticationFlowRepresentation:
    alias: ... = None
    authentication_executions: ... = None
    built_in: ... = None
    description: ... = None
    authentication_flow_representation_id: ... = None
    provider_id: ... = None
    top_level: ... = None

    @classmethod
    def from_dict(cls, item: dict) -> "AuthenticationFlowRepresentation":
        return cls(
            alias=item.get("alias"),
            authentication_executions=item.get("authenticationExecutions"),
            built_in=item.get("builtIn"),
            description=item.get("description"),
            authentication_flow_representation_id=item.get("id"),
            provider_id=item.get("providerId"),
            top_level=item.get("topLevel"),
        )
