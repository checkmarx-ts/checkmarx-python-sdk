# encoding: utf-8


class OIDCClient(object):

    def __init__(self, oidc_client_id, update_access_token_claims_on_refresh, access_token_type, include_jwt_id,
                 always_include_user_claims_in_id_token, client_id, client_name, allow_offline_access,
                 client_secrets, allow_grant_types, allowed_scopes, enabled, require_client_secret, redirect_uris,
                 post_logout_redrect_uris, front_channel_logout_uri, front_channel_logout_session_required,
                 back_channel_logout_uri, back_channel_logout_session_required, identity_token_life_time,
                 access_token_life_time, authorization_code_life_time, absolute_refresh_token_life_time,
                 sliding_refresh_token_life_time, refresh_token_usage, refresh_token_expiration, allowed_cors_origins,
                 allowed_access_tokens_via_browser, claims, client_claims_prefix):
        """

        Args:
            oidc_client_id (int):
            update_access_token_claims_on_refresh (bool):
            access_token_type (int):
            include_jwt_id (bool):
            always_include_user_claims_in_id_token (bool):
            client_id (str):
            client_name (str):
            allow_offline_access (bool):
            client_secrets (list[str]):
            allow_grant_types (list[str]):
            allowed_scopes (list[str]):
            enabled (bool):
            require_client_secret (bool):
            redirect_uris (list):
            post_logout_redrect_uris (list):
            front_channel_logout_uri (str):
            front_channel_logout_session_required (bool):
            back_channel_logout_uri (str):
            back_channel_logout_session_required (bool):
            identity_token_life_time (int):
            access_token_life_time (int):
            authorization_code_life_time (int):
            absolute_refresh_token_life_time (int):
            sliding_refresh_token_life_time (int):
            refresh_token_usage (int):
            refresh_token_expiration (int):
            allowed_cors_origins (list):
            allowed_access_tokens_via_browser (bool):
            claims (list):
            client_claims_prefix (str):
        """
        self.oidc_client_id = oidc_client_id
        self.update_access_token_claims_on_refresh = update_access_token_claims_on_refresh
        self.access_token_type = access_token_type
        self.include_jwt_id = include_jwt_id
        self.always_include_user_claims_in_id_token = always_include_user_claims_in_id_token
        self.client_id = client_id
        self.client_name = client_name
        self.allow_offline_access = allow_offline_access
        self.client_secrets = client_secrets
        self.allow_grant_types = allow_grant_types
        self.allowed_scopes = allowed_scopes
        self.enabled = enabled
        self.require_client_secret = require_client_secret
        self.redirect_uris = redirect_uris
        self.post_logout_redrect_uris = post_logout_redrect_uris
        self.front_channel_logout_uri = front_channel_logout_uri
        self.front_channel_logout_session_required = front_channel_logout_session_required
        self.back_channel_logout_uri = back_channel_logout_uri
        self.back_channel_logout_session_required = back_channel_logout_session_required
        self.identity_token_life_time = identity_token_life_time
        self.access_token_life_time = access_token_life_time
        self.authorization_code_life_time = authorization_code_life_time
        self.absolute_refresh_token_life_time = absolute_refresh_token_life_time
        self.sliding_refresh_token_life_time = sliding_refresh_token_life_time
        self.refresh_token_usage = refresh_token_usage
        self.refresh_token_expiration = refresh_token_expiration
        self.allowed_cors_origins = allowed_cors_origins
        self.allowed_access_tokens_via_browser = allowed_access_tokens_via_browser
        self.claims = claims
        self.client_claims_prefix = client_claims_prefix

    def __str__(self):
        return """OIDCClient(oidc_client_id={}, update_access_token_claims_on_refresh={}, access_token_type={}, 
        include_jwt_id={}, always_include_user_claims_in_id_token={}, client_id={}, client_name={}, 
        allow_offline_access={}, client_secrets={}, allow_grant_types={}, allowed_scopes={}, enabled={}, 
        require_client_secret={}, redirect_uris={}, post_logout_redrect_uris={}, front_channel_logout_uri={}, 
        front_channel_logout_session_required={}, back_channel_logout_uri={}, back_channel_logout_session_required={}, 
        identity_token_life_time={}, access_token_life_time={}, authorization_code_life_time={}, 
        absolute_refresh_token_life_time={}, sliding_refresh_token_life_time={}, refresh_token_usage={}, 
        refresh_token_expiration={}, allowed_cors_origins={}, allowed_access_tokens_via_browser={}, claims={}, 
        client_claims_prefix={})""".format(
            self.oidc_client_id, self.update_access_token_claims_on_refresh, self.access_token_type,
            self.include_jwt_id, self.always_include_user_claims_in_id_token, self.client_id, self.client_name,
            self.allow_offline_access, self.client_secrets, self.allow_grant_types, self.allowed_scopes, self.enabled,
            self.require_client_secret, self.redirect_uris, self.post_logout_redrect_uris,
            self.front_channel_logout_uri, self.front_channel_logout_session_required, self.back_channel_logout_uri,
            self.back_channel_logout_session_required, self.identity_token_life_time,
            self.access_token_life_time, self.authorization_code_life_time, self.absolute_refresh_token_life_time,
            self.sliding_refresh_token_life_time, self.refresh_token_usage, self.refresh_token_expiration,
            self.allowed_cors_origins, self.allowed_access_tokens_via_browser, self.claims, self.client_claims_prefix
        )
