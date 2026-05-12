from dataclasses import dataclass


@dataclass
class IdentityProviderRepresentation:
    add_read_token_role_on_create: ... = None
    alias: ... = None
    config: ... = None
    display_name: ... = None
    enabled: ... = None
    first_broker_login_flow_alias: ... = None
    internal_id: ... = None
    link_only: ... = None
    post_broker_login_flow_alias: ... = None
    provider_id: ... = None
    store_token: ... = None
    trust_email: ... = None

    @classmethod
    def from_dict(cls, item: dict) -> "IdentityProviderRepresentation":
        return cls(
            add_read_token_role_on_create=item.get("addReadTokenRoleOnCreate"),
            alias=item.get("alias"),
            config=item.get("config"),
            display_name=item.get("displayName"),
            enabled=item.get("enabled"),
            first_broker_login_flow_alias=item.get("firstBrokerLoginFlowAlias"),
            internal_id=item.get("internalId"),
            link_only=item.get("linkOnly"),
            post_broker_login_flow_alias=item.get("postBrokerLoginFlowAlias"),
            provider_id=item.get("providerId"),
            store_token=item.get("storeToken"),
            trust_email=item.get("trustEmail"),
        )
