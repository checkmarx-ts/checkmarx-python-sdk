class IdentityProviderRepresentation:
    def __init__(self, add_read_token_role_on_create, alias, config, display_name, enabled,
                 first_broker_login_flow_alias, internal_id, link_only, post_broker_login_flow_alias, provider_id,
                 store_token, trust_email):
        self.addReadTokenRoleOnCreate = add_read_token_role_on_create
        self.alias = alias
        self.config = config
        self.displayName = display_name
        self.enabled = enabled
        self.firstBrokerLoginFlowAlias = first_broker_login_flow_alias
        self.internalId = internal_id
        self.linkOnly = link_only
        self.postBrokerLoginFlowAlias = post_broker_login_flow_alias
        self.providerId = provider_id
        self.storeToken = store_token
        self.trustEmail = trust_email

    def __str__(self):
        return f"IdentityProviderRepresentation(" \
               f"addReadTokenRoleOnCreate={self.addReadTokenRoleOnCreate} " \
               f"alias={self.alias} " \
               f"config={self.config} " \
               f"displayName={self.displayName} " \
               f"enabled={self.enabled} " \
               f"firstBrokerLoginFlowAlias={self.firstBrokerLoginFlowAlias} " \
               f"internalId={self.internalId} " \
               f"linkOnly={self.linkOnly} " \
               f"postBrokerLoginFlowAlias={self.postBrokerLoginFlowAlias} " \
               f"providerId={self.providerId} " \
               f"storeToken={self.storeToken} " \
               f"trustEmail={self.trustEmail} " \
               f")"

    def to_dict(self):
        return {
            "addReadTokenRoleOnCreate": self.addReadTokenRoleOnCreate,
            "alias": self.alias,
            "config": self.config,
            "displayName": self.displayName,
            "enabled": self.enabled,
            "firstBrokerLoginFlowAlias": self.firstBrokerLoginFlowAlias,
            "internalId": self.internalId,
            "linkOnly": self.linkOnly,
            "postBrokerLoginFlowAlias": self.postBrokerLoginFlowAlias,
            "providerId": self.providerId,
            "storeToken": self.storeToken,
            "trustEmail": self.trustEmail,
        }


def construct_identity_provider_representation(item):
    return IdentityProviderRepresentation(
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
