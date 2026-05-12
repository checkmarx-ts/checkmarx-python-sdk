from dataclasses import dataclass
from typing import List, Optional


@dataclass
class OIDCClient:
    id: Optional[int] = None
    update_access_token_claims_on_refresh: Optional[bool] = None
    access_token_type: Optional[int] = None
    include_jwt_id: Optional[bool] = None
    always_include_user_claims_in_id_token: Optional[bool] = None
    client_id: Optional[str] = None
    client_name: Optional[str] = None
    allow_offline_access: Optional[bool] = None
    client_secrets: Optional[List[str]] = None
    allow_grant_types: Optional[List[str]] = None
    allowed_scopes: Optional[List[str]] = None
    enabled: Optional[bool] = None
    require_client_secret: Optional[bool] = None
    redirect_uris: Optional[List[str]] = None
    post_logout_redirect_uris: Optional[List[str]] = None
    front_channel_logout_uri: Optional[str] = None
    front_channel_logout_session_required: Optional[bool] = None
    back_channel_logout_uri: Optional[str] = None
    back_channel_logout_session_required: Optional[bool] = None
    identity_token_life_time: Optional[int] = None
    access_token_life_time: Optional[int] = None
    authorization_code_life_time: Optional[int] = None
    absolute_refresh_token_life_time: Optional[int] = None
    sliding_refresh_token_life_time: Optional[int] = None
    refresh_token_usage: Optional[int] = None
    refresh_token_expiration: Optional[int] = None
    allowed_cors_origins: Optional[List[str]] = None
    allowed_access_tokens_via_browser: Optional[bool] = None
    claims: Optional[List[str]] = None
    client_claims_prefix: Optional[str] = None

    @classmethod
    def from_dict(cls, item: dict) -> "OIDCClient":
        return cls(
            id=item.get("id"),
            update_access_token_claims_on_refresh=item.get("updateAccessTokenClaimsOnRefresh"),
            access_token_type=item.get("accessTokenType"),
            include_jwt_id=item.get("includeJwtId"),
            always_include_user_claims_in_id_token=item.get("alwaysIncludeUserClaimsInIdToken"),
            client_id=item.get("clientId"),
            client_name=item.get("clientName"),
            allow_offline_access=item.get("allowOfflineAccess"),
            client_secrets=item.get("clientSecrets"),
            allow_grant_types=item.get("allowedGrantTypes"),
            allowed_scopes=item.get("allowedScopes"),
            enabled=item.get("enabled"),
            require_client_secret=item.get("requireClientSecret"),
            redirect_uris=item.get("redirectUris"),
            post_logout_redirect_uris=item.get("postLogoutRedirectUris"),
            front_channel_logout_uri=item.get("frontChannelLogoutUri"),
            front_channel_logout_session_required=item.get("frontChannelLogoutSessionRequired"),
            back_channel_logout_uri=item.get("backChannelLogoutUri"),
            back_channel_logout_session_required=item.get("backChannelLogoutSessionRequired"),
            identity_token_life_time=item.get("identityTokenLifetime"),
            access_token_life_time=item.get("accessTokenLifetime"),
            authorization_code_life_time=item.get("authorizationCodeLifetime"),
            absolute_refresh_token_life_time=item.get("absoluteRefreshTokenLifetime"),
            sliding_refresh_token_life_time=item.get("slidingRefreshTokenLifetime"),
            refresh_token_usage=item.get("refreshTokenUsage"),
            refresh_token_expiration=item.get("refreshTokenExpiration"),
            allowed_cors_origins=item.get("allowedCorsOrigins"),
            allowed_access_tokens_via_browser=item.get("allowAccessTokensViaBrowser"),
            claims=item.get("claims"),
            client_claims_prefix=item.get("clientClaimsPrefix"),
        )
