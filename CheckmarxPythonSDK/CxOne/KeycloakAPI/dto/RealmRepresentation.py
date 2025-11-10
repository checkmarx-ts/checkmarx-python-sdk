from dataclasses import dataclass
from typing import Dict, List, Any, Optional
from typing_extensions import Self
from inflection import camelize, underscore
from .ApplicationRepresentation import ApplicationRepresentation
from .AuthenticationFlowRepresentation import AuthenticationFlowRepresentation
from .AuthenticatorConfigRepresentation import AuthenticatorConfigRepresentation
from .ClientPoliciesRepresentation import ClientPoliciesRepresentation
from .ClientProfilesRepresentation import ClientProfilesRepresentation
from .ClientRepresentation import ClientRepresentation
from .ClientScopeRepresentation import ClientScopeRepresentation
from .ClientTemplateRepresentation import ClientTemplateRepresentation
from .GroupRepresentation import GroupRepresentation
from .IdentityProviderMapperRepresentation import IdentityProviderMapperRepresentation
from .IdentityProviderRepresentation import IdentityProviderRepresentation
from .OAuthClientRepresentation import OAuthClientRepresentation
from .ProtocolMapperRepresentation import ProtocolMapperRepresentation
from .RequiredActionProviderRepresentation import RequiredActionProviderRepresentation
from .RoleRepresentation import RoleRepresentation
from .RolesRepresentation import RolesRepresentation
from .ScopeMappingRepresentation import ScopeMappingRepresentation
from .UserFederationMapperRepresentation import UserFederationMapperRepresentation
from .UserFederationProviderRepresentation import UserFederationProviderRepresentation
from .UserRepresentation import UserRepresentation


@dataclass
class RealmRepresentation:
    id: Optional[str] = None
    realm: Optional[str] = None
    display_name: Optional[str] = None
    display_name_html: Optional[str] = None
    not_before: Optional[int] = None
    default_signature_algorithm: Optional[str] = None
    revoke_refresh_token: Optional[bool] = None
    refresh_token_max_reuse: Optional[int] = None
    access_token_lifespan: Optional[int] = None
    access_token_lifespan_for_implicit_flow: Optional[int] = None
    sso_session_idle_timeout: Optional[int] = None
    sso_session_max_lifespan: Optional[int] = None
    sso_session_idle_timeout_remember_me: Optional[int] = None
    sso_session_max_lifespan_remember_me: Optional[int] = None
    offline_session_idle_timeout: Optional[int] = None
    offline_session_max_lifespan_enabled: Optional[bool] = None
    offline_session_max_lifespan: Optional[int] = None
    client_session_idle_timeout: Optional[int] = None
    client_session_max_lifespan: Optional[int] = None
    client_offline_session_idle_timeout: Optional[int] = None
    client_offline_session_max_lifespan: Optional[int] = None
    access_code_lifespan: Optional[int] = None
    access_code_lifespan_user_action: Optional[int] = None
    access_code_lifespan_login: Optional[int] = None
    action_token_generated_by_admin_lifespan: Optional[int] = None
    action_token_generated_by_user_lifespan: Optional[int] = None
    oauth2_device_code_lifespan: Optional[int] = None
    oauth2_device_polling_interval: Optional[int] = None
    enabled: Optional[bool] = None
    ssl_required: Optional[str] = None
    password_credential_grant_allowed: Optional[bool] = None
    registration_allowed: Optional[bool] = None
    registration_email_as_username: Optional[bool] = None
    remember_me: Optional[bool] = None
    verify_email: Optional[bool] = None
    login_with_email_allowed: Optional[bool] = None
    duplicate_emails_allowed: Optional[bool] = None
    reset_password_allowed: Optional[bool] = None
    edit_username_allowed: Optional[bool] = None
    user_cache_enabled: Optional[bool] = None
    realm_cache_enabled: Optional[bool] = None
    brute_force_protected: Optional[bool] = None
    permanent_lockout: Optional[bool] = None
    max_failure_wait_seconds: Optional[int] = None
    minimum_quick_login_wait_seconds: Optional[int] = None
    wait_increment_seconds: Optional[int] = None
    quick_login_check_milli_seconds: Optional[int] = None
    max_delta_time_seconds: Optional[int] = None
    failure_factor: Optional[int] = None
    private_key: Optional[str] = None
    public_key: Optional[str] = None
    certificate: Optional[str] = None
    code_secret: Optional[str] = None
    roles: Optional[RolesRepresentation] = None
    groups: Optional[List[GroupRepresentation]] = None
    default_roles: Optional[List[str]] = None
    default_role: Optional[RoleRepresentation] = None
    default_groups: Optional[List[str]] = None
    required_credentials: Optional[List[str]] = None
    password_policy: Optional[str] = None
    otp_policy_type: Optional[str] = None
    otp_policy_algorithm: Optional[str] = None
    otp_policy_initial_counter: Optional[int] = None
    otp_policy_digits: Optional[int] = None
    otp_policy_look_ahead_window: Optional[int] = None
    otp_policy_period: Optional[int] = None
    otp_policy_code_reusable: Optional[bool] = None
    otp_supported_applications: Optional[List[str]] = None
    localization_texts: Optional[Dict[str, Any]] = None
    web_authn_policy_rp_entity_name: Optional[str] = None
    web_authn_policy_signature_algorithms: Optional[List[str]] = None
    web_authn_policy_rp_id: Optional[str] = None
    web_authn_policy_attestation_conveyance_preference: Optional[str] = None
    web_authn_policy_authenticator_attachment: Optional[str] = None
    web_authn_policy_require_resident_key: Optional[str] = None
    web_authn_policy_user_verification_requirement: Optional[str] = None
    web_authn_policy_create_timeout: Optional[int] = None
    web_authn_policy_avoid_same_authenticator_register: Optional[bool] = None
    web_authn_policy_acceptable_aaguids: Optional[List[str]] = None
    web_authn_policy_extra_origins: Optional[List[str]] = None
    web_authn_policy_passwordless_rp_entity_name: Optional[str] = None
    web_authn_policy_passwordless_signature_algorithms: Optional[List[str]] = None
    web_authn_policy_passwordless_rp_id: Optional[str] = None
    web_authn_policy_passwordless_attestation_conveyance_preference: Optional[str] = None
    web_authn_policy_passwordless_authenticator_attachment: Optional[str] = None
    web_authn_policy_passwordless_require_resident_key: Optional[str] = None
    web_authn_policy_passwordless_user_verification_requirement: Optional[str] = None
    web_authn_policy_passwordless_create_timeout: Optional[int] = None
    web_authn_policy_passwordless_avoid_same_authenticator_register: Optional[bool] = None
    web_authn_policy_passwordless_acceptable_aaguids: Optional[List[str]] = None
    web_authn_policy_passwordless_extra_origins: Optional[List[str]] = None
    client_profiles: Optional[ClientProfilesRepresentation] = None
    client_policies: Optional[ClientPoliciesRepresentation] = None
    users: Optional[List[UserRepresentation]] = None
    federated_users: Optional[List[UserRepresentation]] = None
    scope_mappings: Optional[List[ScopeMappingRepresentation]] = None
    client_scope_mappings: Optional[Dict[str, Any]] = None
    clients: Optional[List[ClientRepresentation]] = None
    client_scopes: Optional[List[ClientScopeRepresentation]] = None
    default_default_client_scopes: Optional[List[str]] = None
    default_optional_client_scopes: Optional[List[str]] = None
    browser_security_headers: Optional[Dict[str, Any]] = None
    smtp_server: Optional[Dict[str, Any]] = None
    user_federation_providers: Optional[List[UserFederationProviderRepresentation]] = None
    user_federation_mappers: Optional[List[UserFederationMapperRepresentation]] = None
    login_theme: Optional[str] = None
    account_theme: Optional[str] = None
    admin_theme: Optional[str] = None
    email_theme: Optional[str] = None
    events_enabled: Optional[bool] = None
    events_expiration: Optional[int] = None
    events_listeners: Optional[List[str]] = None
    enabled_event_types: Optional[List[str]] = None
    admin_events_enabled: Optional[bool] = None
    admin_events_details_enabled: Optional[bool] = None
    identity_providers: Optional[List[IdentityProviderRepresentation]] = None
    identity_provider_mappers: Optional[List[IdentityProviderMapperRepresentation]] = None
    protocol_mappers: Optional[List[ProtocolMapperRepresentation]] = None
    components: Optional[Dict[str, Any]] = None
    internationalization_enabled: Optional[bool] = None
    supported_locales: Optional[List[str]] = None
    default_locale: Optional[str] = None
    authentication_flows: Optional[List[AuthenticationFlowRepresentation]] = None
    authenticator_config: Optional[List[AuthenticatorConfigRepresentation]] = None
    required_actions: Optional[List[RequiredActionProviderRepresentation]] = None
    browser_flow: Optional[str] = None
    registration_flow: Optional[str] = None
    direct_grant_flow: Optional[str] = None
    reset_credentials_flow: Optional[str] = None
    client_authentication_flow: Optional[str] = None
    docker_authentication_flow: Optional[str] = None
    attributes: Optional[Dict[str, Any]] = None
    keycloak_version: Optional[str] = None
    user_managed_access_allowed: Optional[bool] = None
    social: Optional[bool] = None
    update_profile_on_initial_social_login: Optional[bool] = None
    social_providers: Optional[Dict[str, Any]] = None
    application_scope_mappings: Optional[Dict[str, Any]] = None
    applications: Optional[List[ApplicationRepresentation]] = None
    oauth_clients: Optional[List[OAuthClientRepresentation]] = None
    client_templates: Optional[List[ClientTemplateRepresentation]] = None
    o_auth2_device_code_lifespan: Optional[int] = None
    o_auth2_device_polling_interval: Optional[int] = None

    def to_dict(self) -> Dict[str, Any]:
        result: Dict[str, Any] = {}
        if self.id is not None:
            value = self.id
            result['id'] = value
        if self.realm is not None:
            value = self.realm
            result['realm'] = value
        if self.display_name is not None:
            value = self.display_name
            result['displayName'] = value
        if self.display_name_html is not None:
            value = self.display_name_html
            result['displayNameHtml'] = value
        if self.not_before is not None:
            value = self.not_before
            result['notBefore'] = value
        if self.default_signature_algorithm is not None:
            value = self.default_signature_algorithm
            result['defaultSignatureAlgorithm'] = value
        if self.revoke_refresh_token is not None:
            value = self.revoke_refresh_token
            result['revokeRefreshToken'] = value
        if self.refresh_token_max_reuse is not None:
            value = self.refresh_token_max_reuse
            result['refreshTokenMaxReuse'] = value
        if self.access_token_lifespan is not None:
            value = self.access_token_lifespan
            result['accessTokenLifespan'] = value
        if self.access_token_lifespan_for_implicit_flow is not None:
            value = self.access_token_lifespan_for_implicit_flow
            result['accessTokenLifespanForImplicitFlow'] = value
        if self.sso_session_idle_timeout is not None:
            value = self.sso_session_idle_timeout
            result['ssoSessionIdleTimeout'] = value
        if self.sso_session_max_lifespan is not None:
            value = self.sso_session_max_lifespan
            result['ssoSessionMaxLifespan'] = value
        if self.sso_session_idle_timeout_remember_me is not None:
            value = self.sso_session_idle_timeout_remember_me
            result['ssoSessionIdleTimeoutRememberMe'] = value
        if self.sso_session_max_lifespan_remember_me is not None:
            value = self.sso_session_max_lifespan_remember_me
            result['ssoSessionMaxLifespanRememberMe'] = value
        if self.offline_session_idle_timeout is not None:
            value = self.offline_session_idle_timeout
            result['offlineSessionIdleTimeout'] = value
        if self.offline_session_max_lifespan_enabled is not None:
            value = self.offline_session_max_lifespan_enabled
            result['offlineSessionMaxLifespanEnabled'] = value
        if self.offline_session_max_lifespan is not None:
            value = self.offline_session_max_lifespan
            result['offlineSessionMaxLifespan'] = value
        if self.client_session_idle_timeout is not None:
            value = self.client_session_idle_timeout
            result['clientSessionIdleTimeout'] = value
        if self.client_session_max_lifespan is not None:
            value = self.client_session_max_lifespan
            result['clientSessionMaxLifespan'] = value
        if self.client_offline_session_idle_timeout is not None:
            value = self.client_offline_session_idle_timeout
            result['clientOfflineSessionIdleTimeout'] = value
        if self.client_offline_session_max_lifespan is not None:
            value = self.client_offline_session_max_lifespan
            result['clientOfflineSessionMaxLifespan'] = value
        if self.access_code_lifespan is not None:
            value = self.access_code_lifespan
            result['accessCodeLifespan'] = value
        if self.access_code_lifespan_user_action is not None:
            value = self.access_code_lifespan_user_action
            result['accessCodeLifespanUserAction'] = value
        if self.access_code_lifespan_login is not None:
            value = self.access_code_lifespan_login
            result['accessCodeLifespanLogin'] = value
        if self.action_token_generated_by_admin_lifespan is not None:
            value = self.action_token_generated_by_admin_lifespan
            result['actionTokenGeneratedByAdminLifespan'] = value
        if self.action_token_generated_by_user_lifespan is not None:
            value = self.action_token_generated_by_user_lifespan
            result['actionTokenGeneratedByUserLifespan'] = value
        if self.oauth2_device_code_lifespan is not None:
            value = self.oauth2_device_code_lifespan
            result['oauth2DeviceCodeLifespan'] = value
        if self.oauth2_device_polling_interval is not None:
            value = self.oauth2_device_polling_interval
            result['oauth2DevicePollingInterval'] = value
        if self.enabled is not None:
            value = self.enabled
            result['enabled'] = value
        if self.ssl_required is not None:
            value = self.ssl_required
            result['sslRequired'] = value
        if self.password_credential_grant_allowed is not None:
            value = self.password_credential_grant_allowed
            result['passwordCredentialGrantAllowed'] = value
        if self.registration_allowed is not None:
            value = self.registration_allowed
            result['registrationAllowed'] = value
        if self.registration_email_as_username is not None:
            value = self.registration_email_as_username
            result['registrationEmailAsUsername'] = value
        if self.remember_me is not None:
            value = self.remember_me
            result['rememberMe'] = value
        if self.verify_email is not None:
            value = self.verify_email
            result['verifyEmail'] = value
        if self.login_with_email_allowed is not None:
            value = self.login_with_email_allowed
            result['loginWithEmailAllowed'] = value
        if self.duplicate_emails_allowed is not None:
            value = self.duplicate_emails_allowed
            result['duplicateEmailsAllowed'] = value
        if self.reset_password_allowed is not None:
            value = self.reset_password_allowed
            result['resetPasswordAllowed'] = value
        if self.edit_username_allowed is not None:
            value = self.edit_username_allowed
            result['editUsernameAllowed'] = value
        if self.user_cache_enabled is not None:
            value = self.user_cache_enabled
            result['userCacheEnabled'] = value
        if self.realm_cache_enabled is not None:
            value = self.realm_cache_enabled
            result['realmCacheEnabled'] = value
        if self.brute_force_protected is not None:
            value = self.brute_force_protected
            result['bruteForceProtected'] = value
        if self.permanent_lockout is not None:
            value = self.permanent_lockout
            result['permanentLockout'] = value
        if self.max_failure_wait_seconds is not None:
            value = self.max_failure_wait_seconds
            result['maxFailureWaitSeconds'] = value
        if self.minimum_quick_login_wait_seconds is not None:
            value = self.minimum_quick_login_wait_seconds
            result['minimumQuickLoginWaitSeconds'] = value
        if self.wait_increment_seconds is not None:
            value = self.wait_increment_seconds
            result['waitIncrementSeconds'] = value
        if self.quick_login_check_milli_seconds is not None:
            value = self.quick_login_check_milli_seconds
            result['quickLoginCheckMilliSeconds'] = value
        if self.max_delta_time_seconds is not None:
            value = self.max_delta_time_seconds
            result['maxDeltaTimeSeconds'] = value
        if self.failure_factor is not None:
            value = self.failure_factor
            result['failureFactor'] = value
        if self.private_key is not None:
            value = self.private_key
            result['privateKey'] = value
        if self.public_key is not None:
            value = self.public_key
            result['publicKey'] = value
        if self.certificate is not None:
            value = self.certificate
            result['certificate'] = value
        if self.code_secret is not None:
            value = self.code_secret
            result['codeSecret'] = value
        if self.roles is not None:
            value = self.roles.to_dict()
            result['roles'] = value
        if self.groups is not None:
            value = [item.to_dict() for item in self.groups]
            result['groups'] = value
        if self.default_roles is not None:
            value = self.default_roles
            result['defaultRoles'] = value
        if self.default_role is not None:
            value = self.default_role.to_dict()
            result['defaultRole'] = value
        if self.default_groups is not None:
            value = self.default_groups
            result['defaultGroups'] = value
        if self.required_credentials is not None:
            value = self.required_credentials
            result['requiredCredentials'] = value
        if self.password_policy is not None:
            value = self.password_policy
            result['passwordPolicy'] = value
        if self.otp_policy_type is not None:
            value = self.otp_policy_type
            result['otpPolicyType'] = value
        if self.otp_policy_algorithm is not None:
            value = self.otp_policy_algorithm
            result['otpPolicyAlgorithm'] = value
        if self.otp_policy_initial_counter is not None:
            value = self.otp_policy_initial_counter
            result['otpPolicyInitialCounter'] = value
        if self.otp_policy_digits is not None:
            value = self.otp_policy_digits
            result['otpPolicyDigits'] = value
        if self.otp_policy_look_ahead_window is not None:
            value = self.otp_policy_look_ahead_window
            result['otpPolicyLookAheadWindow'] = value
        if self.otp_policy_period is not None:
            value = self.otp_policy_period
            result['otpPolicyPeriod'] = value
        if self.otp_policy_code_reusable is not None:
            value = self.otp_policy_code_reusable
            result['otpPolicyCodeReusable'] = value
        if self.otp_supported_applications is not None:
            value = self.otp_supported_applications
            result['otpSupportedApplications'] = value
        if self.localization_texts is not None:
            value = self.localization_texts
            result['localizationTexts'] = value
        if self.web_authn_policy_rp_entity_name is not None:
            value = self.web_authn_policy_rp_entity_name
            result['webAuthnPolicyRpEntityName'] = value
        if self.web_authn_policy_signature_algorithms is not None:
            value = self.web_authn_policy_signature_algorithms
            result['webAuthnPolicySignatureAlgorithms'] = value
        if self.web_authn_policy_rp_id is not None:
            value = self.web_authn_policy_rp_id
            result['webAuthnPolicyRpId'] = value
        if self.web_authn_policy_attestation_conveyance_preference is not None:
            value = self.web_authn_policy_attestation_conveyance_preference
            result['webAuthnPolicyAttestationConveyancePreference'] = value
        if self.web_authn_policy_authenticator_attachment is not None:
            value = self.web_authn_policy_authenticator_attachment
            result['webAuthnPolicyAuthenticatorAttachment'] = value
        if self.web_authn_policy_require_resident_key is not None:
            value = self.web_authn_policy_require_resident_key
            result['webAuthnPolicyRequireResidentKey'] = value
        if self.web_authn_policy_user_verification_requirement is not None:
            value = self.web_authn_policy_user_verification_requirement
            result['webAuthnPolicyUserVerificationRequirement'] = value
        if self.web_authn_policy_create_timeout is not None:
            value = self.web_authn_policy_create_timeout
            result['webAuthnPolicyCreateTimeout'] = value
        if self.web_authn_policy_avoid_same_authenticator_register is not None:
            value = self.web_authn_policy_avoid_same_authenticator_register
            result['webAuthnPolicyAvoidSameAuthenticatorRegister'] = value
        if self.web_authn_policy_acceptable_aaguids is not None:
            value = self.web_authn_policy_acceptable_aaguids
            result['webAuthnPolicyAcceptableAaguids'] = value
        if self.web_authn_policy_extra_origins is not None:
            value = self.web_authn_policy_extra_origins
            result['webAuthnPolicyExtraOrigins'] = value
        if self.web_authn_policy_passwordless_rp_entity_name is not None:
            value = self.web_authn_policy_passwordless_rp_entity_name
            result['webAuthnPolicyPasswordlessRpEntityName'] = value
        if self.web_authn_policy_passwordless_signature_algorithms is not None:
            value = self.web_authn_policy_passwordless_signature_algorithms
            result['webAuthnPolicyPasswordlessSignatureAlgorithms'] = value
        if self.web_authn_policy_passwordless_rp_id is not None:
            value = self.web_authn_policy_passwordless_rp_id
            result['webAuthnPolicyPasswordlessRpId'] = value
        if self.web_authn_policy_passwordless_attestation_conveyance_preference is not None:
            value = self.web_authn_policy_passwordless_attestation_conveyance_preference
            result['webAuthnPolicyPasswordlessAttestationConveyancePreference'] = value
        if self.web_authn_policy_passwordless_authenticator_attachment is not None:
            value = self.web_authn_policy_passwordless_authenticator_attachment
            result['webAuthnPolicyPasswordlessAuthenticatorAttachment'] = value
        if self.web_authn_policy_passwordless_require_resident_key is not None:
            value = self.web_authn_policy_passwordless_require_resident_key
            result['webAuthnPolicyPasswordlessRequireResidentKey'] = value
        if self.web_authn_policy_passwordless_user_verification_requirement is not None:
            value = self.web_authn_policy_passwordless_user_verification_requirement
            result['webAuthnPolicyPasswordlessUserVerificationRequirement'] = value
        if self.web_authn_policy_passwordless_create_timeout is not None:
            value = self.web_authn_policy_passwordless_create_timeout
            result['webAuthnPolicyPasswordlessCreateTimeout'] = value
        if self.web_authn_policy_passwordless_avoid_same_authenticator_register is not None:
            value = self.web_authn_policy_passwordless_avoid_same_authenticator_register
            result['webAuthnPolicyPasswordlessAvoidSameAuthenticatorRegister'] = value
        if self.web_authn_policy_passwordless_acceptable_aaguids is not None:
            value = self.web_authn_policy_passwordless_acceptable_aaguids
            result['webAuthnPolicyPasswordlessAcceptableAaguids'] = value
        if self.web_authn_policy_passwordless_extra_origins is not None:
            value = self.web_authn_policy_passwordless_extra_origins
            result['webAuthnPolicyPasswordlessExtraOrigins'] = value
        if self.client_profiles is not None:
            value = self.client_profiles.to_dict()
            result['clientProfiles'] = value
        if self.client_policies is not None:
            value = self.client_policies.to_dict()
            result['clientPolicies'] = value
        if self.users is not None:
            value = [item.to_dict() for item in self.users]
            result['users'] = value
        if self.federated_users is not None:
            value = [item.to_dict() for item in self.federated_users]
            result['federatedUsers'] = value
        if self.scope_mappings is not None:
            value = [item.to_dict() for item in self.scope_mappings]
            result['scopeMappings'] = value
        if self.client_scope_mappings is not None:
            value = self.client_scope_mappings
            result['clientScopeMappings'] = value
        if self.clients is not None:
            value = [item.to_dict() for item in self.clients]
            result['clients'] = value
        if self.client_scopes is not None:
            value = [item.to_dict() for item in self.client_scopes]
            result['clientScopes'] = value
        if self.default_default_client_scopes is not None:
            value = self.default_default_client_scopes
            result['defaultDefaultClientScopes'] = value
        if self.default_optional_client_scopes is not None:
            value = self.default_optional_client_scopes
            result['defaultOptionalClientScopes'] = value
        if self.browser_security_headers is not None:
            value = self.browser_security_headers
            result['browserSecurityHeaders'] = value
        if self.smtp_server is not None:
            value = self.smtp_server
            result['smtpServer'] = value
        if self.user_federation_providers is not None:
            value = [item.to_dict() for item in self.user_federation_providers]
            result['userFederationProviders'] = value
        if self.user_federation_mappers is not None:
            value = [item.to_dict() for item in self.user_federation_mappers]
            result['userFederationMappers'] = value
        if self.login_theme is not None:
            value = self.login_theme
            result['loginTheme'] = value
        if self.account_theme is not None:
            value = self.account_theme
            result['accountTheme'] = value
        if self.admin_theme is not None:
            value = self.admin_theme
            result['adminTheme'] = value
        if self.email_theme is not None:
            value = self.email_theme
            result['emailTheme'] = value
        if self.events_enabled is not None:
            value = self.events_enabled
            result['eventsEnabled'] = value
        if self.events_expiration is not None:
            value = self.events_expiration
            result['eventsExpiration'] = value
        if self.events_listeners is not None:
            value = self.events_listeners
            result['eventsListeners'] = value
        if self.enabled_event_types is not None:
            value = self.enabled_event_types
            result['enabledEventTypes'] = value
        if self.admin_events_enabled is not None:
            value = self.admin_events_enabled
            result['adminEventsEnabled'] = value
        if self.admin_events_details_enabled is not None:
            value = self.admin_events_details_enabled
            result['adminEventsDetailsEnabled'] = value
        if self.identity_providers is not None:
            value = [item.to_dict() for item in self.identity_providers]
            result['identityProviders'] = value
        if self.identity_provider_mappers is not None:
            value = [item.to_dict() for item in self.identity_provider_mappers]
            result['identityProviderMappers'] = value
        if self.protocol_mappers is not None:
            value = [item.to_dict() for item in self.protocol_mappers]
            result['protocolMappers'] = value
        if self.components is not None:
            value = self.components
            result['components'] = value
        if self.internationalization_enabled is not None:
            value = self.internationalization_enabled
            result['internationalizationEnabled'] = value
        if self.supported_locales is not None:
            value = self.supported_locales
            result['supportedLocales'] = value
        if self.default_locale is not None:
            value = self.default_locale
            result['defaultLocale'] = value
        if self.authentication_flows is not None:
            value = [item.to_dict() for item in self.authentication_flows]
            result['authenticationFlows'] = value
        if self.authenticator_config is not None:
            value = [item.to_dict() for item in self.authenticator_config]
            result['authenticatorConfig'] = value
        if self.required_actions is not None:
            value = [item.to_dict() for item in self.required_actions]
            result['requiredActions'] = value
        if self.browser_flow is not None:
            value = self.browser_flow
            result['browserFlow'] = value
        if self.registration_flow is not None:
            value = self.registration_flow
            result['registrationFlow'] = value
        if self.direct_grant_flow is not None:
            value = self.direct_grant_flow
            result['directGrantFlow'] = value
        if self.reset_credentials_flow is not None:
            value = self.reset_credentials_flow
            result['resetCredentialsFlow'] = value
        if self.client_authentication_flow is not None:
            value = self.client_authentication_flow
            result['clientAuthenticationFlow'] = value
        if self.docker_authentication_flow is not None:
            value = self.docker_authentication_flow
            result['dockerAuthenticationFlow'] = value
        if self.attributes is not None:
            value = self.attributes
            result['attributes'] = value
        if self.keycloak_version is not None:
            value = self.keycloak_version
            result['keycloakVersion'] = value
        if self.user_managed_access_allowed is not None:
            value = self.user_managed_access_allowed
            result['userManagedAccessAllowed'] = value
        if self.social is not None:
            value = self.social
            result['social'] = value
        if self.update_profile_on_initial_social_login is not None:
            value = self.update_profile_on_initial_social_login
            result['updateProfileOnInitialSocialLogin'] = value
        if self.social_providers is not None:
            value = self.social_providers
            result['socialProviders'] = value
        if self.application_scope_mappings is not None:
            value = self.application_scope_mappings
            result['applicationScopeMappings'] = value
        if self.applications is not None:
            value = [item.to_dict() for item in self.applications]
            result['applications'] = value
        if self.oauth_clients is not None:
            value = [item.to_dict() for item in self.oauth_clients]
            result['oauthClients'] = value
        if self.client_templates is not None:
            value = [item.to_dict() for item in self.client_templates]
            result['clientTemplates'] = value
        if self.o_auth2_device_code_lifespan is not None:
            value = self.o_auth2_device_code_lifespan
            result['oAuth2DeviceCodeLifespan'] = value
        if self.o_auth2_device_polling_interval is not None:
            value = self.o_auth2_device_polling_interval
            result['oAuth2DevicePollingInterval'] = value
        return result

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> Self:
        snake_data: Dict[str, Any] = {underscore(k): v for k, v in data.items()}

        if 'roles' in snake_data and snake_data['roles'] is not None:
            snake_data['roles'] = RolesRepresentation.from_dict(snake_data['roles'])
        if 'default_role' in snake_data and snake_data['default_role'] is not None:
            snake_data['default_role'] = RoleRepresentation.from_dict(snake_data['default_role'])
        if 'client_profiles' in snake_data and snake_data['client_profiles'] is not None:
            snake_data['client_profiles'] = ClientProfilesRepresentation.from_dict(snake_data['client_profiles'])
        if 'client_policies' in snake_data and snake_data['client_policies'] is not None:
            snake_data['client_policies'] = ClientPoliciesRepresentation.from_dict(snake_data['client_policies'])
        if 'groups' in snake_data and snake_data['groups'] is not None:
            snake_data['groups'] = [
                GroupRepresentation.from_dict(item) for item in snake_data['groups']
            ]
        if 'users' in snake_data and snake_data['users'] is not None:
            snake_data['users'] = [
                UserRepresentation.from_dict(item) for item in snake_data['users']
            ]
        if 'federated_users' in snake_data and snake_data['federated_users'] is not None:
            snake_data['federated_users'] = [
                UserRepresentation.from_dict(item) for item in snake_data['federated_users']
            ]
        if 'scope_mappings' in snake_data and snake_data['scope_mappings'] is not None:
            snake_data['scope_mappings'] = [
                ScopeMappingRepresentation.from_dict(item) for item in snake_data['scope_mappings']
            ]
        if 'clients' in snake_data and snake_data['clients'] is not None:
            snake_data['clients'] = [
                ClientRepresentation.from_dict(item) for item in snake_data['clients']
            ]
        if 'client_scopes' in snake_data and snake_data['client_scopes'] is not None:
            snake_data['client_scopes'] = [
                ClientScopeRepresentation.from_dict(item) for item in snake_data['client_scopes']
            ]
        if 'user_federation_providers' in snake_data and snake_data['user_federation_providers'] is not None:
            snake_data['user_federation_providers'] = [
                UserFederationProviderRepresentation.from_dict(item) for item in snake_data['user_federation_providers']
            ]
        if 'user_federation_mappers' in snake_data and snake_data['user_federation_mappers'] is not None:
            snake_data['user_federation_mappers'] = [
                UserFederationMapperRepresentation.from_dict(item) for item in snake_data['user_federation_mappers']
            ]
        if 'identity_providers' in snake_data and snake_data['identity_providers'] is not None:
            snake_data['identity_providers'] = [
                IdentityProviderRepresentation.from_dict(item) for item in snake_data['identity_providers']
            ]
        if 'identity_provider_mappers' in snake_data and snake_data['identity_provider_mappers'] is not None:
            snake_data['identity_provider_mappers'] = [
                IdentityProviderMapperRepresentation.from_dict(item) for item in snake_data['identity_provider_mappers']
            ]
        if 'protocol_mappers' in snake_data and snake_data['protocol_mappers'] is not None:
            snake_data['protocol_mappers'] = [
                ProtocolMapperRepresentation.from_dict(item) for item in snake_data['protocol_mappers']
            ]
        if 'authentication_flows' in snake_data and snake_data['authentication_flows'] is not None:
            snake_data['authentication_flows'] = [
                AuthenticationFlowRepresentation.from_dict(item) for item in snake_data['authentication_flows']
            ]
        if 'authenticator_config' in snake_data and snake_data['authenticator_config'] is not None:
            snake_data['authenticator_config'] = [
                AuthenticatorConfigRepresentation.from_dict(item) for item in snake_data['authenticator_config']
            ]
        if 'required_actions' in snake_data and snake_data['required_actions'] is not None:
            snake_data['required_actions'] = [
                RequiredActionProviderRepresentation.from_dict(item) for item in snake_data['required_actions']
            ]
        if 'applications' in snake_data and snake_data['applications'] is not None:
            snake_data['applications'] = [
                ApplicationRepresentation.from_dict(item) for item in snake_data['applications']
            ]
        if 'oauth_clients' in snake_data and snake_data['oauth_clients'] is not None:
            snake_data['oauth_clients'] = [
                OAuthClientRepresentation.from_dict(item) for item in snake_data['oauth_clients']
            ]
        if 'client_templates' in snake_data and snake_data['client_templates'] is not None:
            snake_data['client_templates'] = [
                ClientTemplateRepresentation.from_dict(item) for item in snake_data['client_templates']
            ]
        required_fields = []
        missing = [f for f in required_fields if f not in snake_data]
        if missing:
            raise ValueError(f'missing required field: {missing}')
        return cls(**snake_data)
