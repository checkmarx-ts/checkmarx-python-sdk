from dataclasses import dataclass


@dataclass
class AuthenticationExecutionInfoRepresentation:
    alias: ... = None
    authentication_config: ... = None
    authentication_flow: ... = None
    configurable: ... = None
    description: ... = None
    display_name: ... = None
    flow_id: ... = None
    authentication_execution_info_representation_id: ... = None
    index: ... = None
    level: ... = None
    provider_id: ... = None
    requirement: ... = None
    requirement_choices: ... = None

    @classmethod
    def from_dict(cls, item: dict) -> "AuthenticationExecutionInfoRepresentation":
        return cls(
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
