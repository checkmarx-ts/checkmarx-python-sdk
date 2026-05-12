from dataclasses import dataclass


@dataclass
class RealmRepresentation:
    access_code_lifespan: ... = None
    access_code_lifespan_login: ... = None
    access_code_lifespan_user_action: ... = None
    access_token_lifespan: ... = None
    access_token_lifespan_for_implicit_flow: ... = None
    account_theme: ... = None
    action_token_generated_by_admin_lifespan: ... = None
    action_token_generated_by_user_lifespan: ... = None
    admin_events_details_enabled: ... = None
    admin_events_enabled: ... = None
    admin_theme: ... = None
    attributes: ... = None
    authentication_flows: ... = None
    authenticator_config: ... = None
    browser_flow: ... = None
    browser_security_headers: ... = None
    brute_force_protected: ... = None
    client_authentication_flow: ... = None
    client_offline_session_idle_timeout: ... = None
    client_offline_session_max_lifespan: ... = None
    client_policies: ... = None
    client_profiles: ... = None
    client_scope_mappings: ... = None
    client_scopes: ... = None
    client_session_idle_timeout: ... = None
    client_session_max_lifespan: ... = None
    clients: ... = None
    components: ... = None
    default_default_client_scopes: ... = None
    default_groups: ... = None
    default_locale: ... = None
    default_optional_client_scopes: ... = None
    default_role: ... = None
    default_signature_algorithm: ... = None
    direct_grant_flow: ... = None
    display_name: ... = None
    display_name_html: ... = None
    docker_authentication_flow: ... = None
    duplicate_emails_allowed: ... = None
    edit_username_allowed: ... = None
    email_theme: ... = None
    enabled: ... = None
    enabled_event_types: ... = None
    events_enabled: ... = None
    events_expiration: ... = None
    events_listeners: ... = None
    failure_factor: ... = None
    federated_users: ... = None
    groups: ... = None
    realm_representation_id: ... = None
    identity_provider_mappers: ... = None
    identity_providers: ... = None
    internationalization_enabled: ... = None
    keycloak_version: ... = None
    login_theme: ... = None
    login_with_email_allowed: ... = None
    max_delta_time_seconds: ... = None
    max_failure_wait_seconds: ... = None
    minimum_quick_login_wait_seconds: ... = None
    not_before: ... = None
    o_auth2_device_code_lifespan: ... = None
    o_auth2_device_polling_interval: ... = None
    oauth2_device_code_lifespan: ... = None
    oauth2_device_polling_interval: ... = None
    offline_session_idle_timeout: ... = None
    offline_session_max_lifespan: ... = None
    offline_session_max_lifespan_enabled: ... = None
    otp_policy_algorithm: ... = None
    otp_policy_digits: ... = None
    otp_policy_initial_counter: ... = None
    otp_policy_look_ahead_window: ... = None
    otp_policy_period: ... = None
    otp_policy_type: ... = None
    otp_supported_applications: ... = None
    password_policy: ... = None
    permanent_lockout: ... = None
    protocol_mappers: ... = None
    quick_login_check_milli_seconds: ... = None
    realm: ... = None
    refresh_token_max_reuse: ... = None
    registration_allowed: ... = None
    registration_email_as_username: ... = None
    registration_flow: ... = None
    remember_me: ... = None
    required_actions: ... = None
    reset_credentials_flow: ... = None
    reset_password_allowed: ... = None
    revoke_refresh_token: ... = None
    roles: ... = None
    scope_mappings: ... = None
    smtp_server: ... = None
    ssl_required: ... = None
    sso_session_idle_timeout: ... = None
    sso_session_idle_timeout_remember_me: ... = None
    sso_session_max_lifespan: ... = None
    sso_session_max_lifespan_remember_me: ... = None
    supported_locales: ... = None
    user_federation_mappers: ... = None
    user_federation_providers: ... = None
    user_managed_access_allowed: ... = None
    users: ... = None
    verify_email: ... = None
    wait_increment_seconds: ... = None
    web_authn_policy_acceptable_aaguids: ... = None
    web_authn_policy_attestation_conveyance_preference: ... = None
    web_authn_policy_authenticator_attachment: ... = None
    web_authn_policy_avoid_same_authenticator_register: ... = None
    web_authn_policy_create_timeout: ... = None
    web_authn_policy_passwordless_acceptable_aaguids: ... = None
    web_authn_policy_passwordless_attestation_conveyance_preference: ... = None
    web_authn_policy_passwordless_authenticator_attachment: ... = None
    web_authn_policy_passwordless_avoid_same_authenticator_register: ... = None
    web_authn_policy_passwordless_create_timeout: ... = None
    web_authn_policy_passwordless_require_resident_key: ... = None
    web_authn_policy_passwordless_rp_entity_name: ... = None
    web_authn_policy_passwordless_rp_id: ... = None
    web_authn_policy_passwordless_signature_algorithms: ... = None
    web_authn_policy_passwordless_user_verification_requirement: ... = None
    web_authn_policy_require_resident_key: ... = None
    web_authn_policy_rp_entity_name: ... = None
    web_authn_policy_rp_id: ... = None
    web_authn_policy_signature_algorithms: ... = None
    web_authn_policy_user_verification_requirement: ... = None

    @classmethod
    def from_dict(cls, item: dict) -> "RealmRepresentation":
        return cls(
            access_code_lifespan=item.get("accessCodeLifespan"),
            access_code_lifespan_login=item.get("accessCodeLifespanLogin"),
            access_code_lifespan_user_action=item.get("accessCodeLifespanUserAction"),
            access_token_lifespan=item.get("accessTokenLifespan"),
            access_token_lifespan_for_implicit_flow=item.get(
                "accessTokenLifespanForImplicitFlow"
            ),
            account_theme=item.get("accountTheme"),
            action_token_generated_by_admin_lifespan=item.get(
                "actionTokenGeneratedByAdminLifespan"
            ),
            action_token_generated_by_user_lifespan=item.get(
                "actionTokenGeneratedByUserLifespan"
            ),
            admin_events_details_enabled=item.get("adminEventsDetailsEnabled"),
            admin_events_enabled=item.get("adminEventsEnabled"),
            admin_theme=item.get("adminTheme"),
            attributes=item.get("attributes"),
            authentication_flows=item.get("authenticationFlows"),
            authenticator_config=item.get("authenticatorConfig"),
            browser_flow=item.get("browserFlow"),
            browser_security_headers=item.get("browserSecurityHeaders"),
            brute_force_protected=item.get("bruteForceProtected"),
            client_authentication_flow=item.get("clientAuthenticationFlow"),
            client_offline_session_idle_timeout=item.get(
                "clientOfflineSessionIdleTimeout"
            ),
            client_offline_session_max_lifespan=item.get(
                "clientOfflineSessionMaxLifespan"
            ),
            client_policies=item.get("clientPolicies"),
            client_profiles=item.get("clientProfiles"),
            client_scope_mappings=item.get("clientScopeMappings"),
            client_scopes=item.get("clientScopes"),
            client_session_idle_timeout=item.get("clientSessionIdleTimeout"),
            client_session_max_lifespan=item.get("clientSessionMaxLifespan"),
            clients=item.get("clients"),
            components=item.get("components"),
            default_default_client_scopes=item.get("defaultDefaultClientScopes"),
            default_groups=item.get("defaultGroups"),
            default_locale=item.get("defaultLocale"),
            default_optional_client_scopes=item.get("defaultOptionalClientScopes"),
            default_role=item.get("defaultRole"),
            default_signature_algorithm=item.get("defaultSignatureAlgorithm"),
            direct_grant_flow=item.get("directGrantFlow"),
            display_name=item.get("displayName"),
            display_name_html=item.get("displayNameHtml"),
            docker_authentication_flow=item.get("dockerAuthenticationFlow"),
            duplicate_emails_allowed=item.get("duplicateEmailsAllowed"),
            edit_username_allowed=item.get("editUsernameAllowed"),
            email_theme=item.get("emailTheme"),
            enabled=item.get("enabled"),
            enabled_event_types=item.get("enabledEventTypes"),
            events_enabled=item.get("eventsEnabled"),
            events_expiration=item.get("eventsExpiration"),
            events_listeners=item.get("eventsListeners"),
            failure_factor=item.get("failureFactor"),
            federated_users=item.get("federatedUsers"),
            groups=item.get("groups"),
            realm_representation_id=item.get("id"),
            identity_provider_mappers=item.get("identityProviderMappers"),
            identity_providers=item.get("identityProviders"),
            internationalization_enabled=item.get("internationalizationEnabled"),
            keycloak_version=item.get("keycloakVersion"),
            login_theme=item.get("loginTheme"),
            login_with_email_allowed=item.get("loginWithEmailAllowed"),
            max_delta_time_seconds=item.get("maxDeltaTimeSeconds"),
            max_failure_wait_seconds=item.get("maxFailureWaitSeconds"),
            minimum_quick_login_wait_seconds=item.get("minimumQuickLoginWaitSeconds"),
            not_before=item.get("notBefore"),
            o_auth2_device_code_lifespan=item.get("oAuth2DeviceCodeLifespan"),
            o_auth2_device_polling_interval=item.get("oAuth2DevicePollingInterval"),
            oauth2_device_code_lifespan=item.get("oauth2DeviceCodeLifespan"),
            oauth2_device_polling_interval=item.get("oauth2DevicePollingInterval"),
            offline_session_idle_timeout=item.get("offlineSessionIdleTimeout"),
            offline_session_max_lifespan=item.get("offlineSessionMaxLifespan"),
            offline_session_max_lifespan_enabled=item.get(
                "offlineSessionMaxLifespanEnabled"
            ),
            otp_policy_algorithm=item.get("otpPolicyAlgorithm"),
            otp_policy_digits=item.get("otpPolicyDigits"),
            otp_policy_initial_counter=item.get("otpPolicyInitialCounter"),
            otp_policy_look_ahead_window=item.get("otpPolicyLookAheadWindow"),
            otp_policy_period=item.get("otpPolicyPeriod"),
            otp_policy_type=item.get("otpPolicyType"),
            otp_supported_applications=item.get("otpSupportedApplications"),
            password_policy=item.get("passwordPolicy"),
            permanent_lockout=item.get("permanentLockout"),
            protocol_mappers=item.get("protocolMappers"),
            quick_login_check_milli_seconds=item.get("quickLoginCheckMilliSeconds"),
            realm=item.get("realm"),
            refresh_token_max_reuse=item.get("refreshTokenMaxReuse"),
            registration_allowed=item.get("registrationAllowed"),
            registration_email_as_username=item.get("registrationEmailAsUsername"),
            registration_flow=item.get("registrationFlow"),
            remember_me=item.get("rememberMe"),
            required_actions=item.get("requiredActions"),
            reset_credentials_flow=item.get("resetCredentialsFlow"),
            reset_password_allowed=item.get("resetPasswordAllowed"),
            revoke_refresh_token=item.get("revokeRefreshToken"),
            roles=item.get("roles"),
            scope_mappings=item.get("scopeMappings"),
            smtp_server=item.get("smtpServer"),
            ssl_required=item.get("sslRequired"),
            sso_session_idle_timeout=item.get("ssoSessionIdleTimeout"),
            sso_session_idle_timeout_remember_me=item.get(
                "ssoSessionIdleTimeoutRememberMe"
            ),
            sso_session_max_lifespan=item.get("ssoSessionMaxLifespan"),
            sso_session_max_lifespan_remember_me=item.get(
                "ssoSessionMaxLifespanRememberMe"
            ),
            supported_locales=item.get("supportedLocales"),
            user_federation_mappers=item.get("userFederationMappers"),
            user_federation_providers=item.get("userFederationProviders"),
            user_managed_access_allowed=item.get("userManagedAccessAllowed"),
            users=item.get("users"),
            verify_email=item.get("verifyEmail"),
            wait_increment_seconds=item.get("waitIncrementSeconds"),
            web_authn_policy_acceptable_aaguids=item.get(
                "webAuthnPolicyAcceptableAaguids"
            ),
            web_authn_policy_attestation_conveyance_preference=item.get(
                "webAuthnPolicyAttestationConveyancePreference"
            ),
            web_authn_policy_authenticator_attachment=item.get(
                "webAuthnPolicyAuthenticatorAttachment"
            ),
            web_authn_policy_avoid_same_authenticator_register=item.get(
                "webAuthnPolicyAvoidSameAuthenticatorRegister"
            ),
            web_authn_policy_create_timeout=item.get("webAuthnPolicyCreateTimeout"),
            web_authn_policy_passwordless_acceptable_aaguids=item.get(
                "webAuthnPolicyPasswordlessAcceptableAaguids"
            ),
            web_authn_policy_passwordless_attestation_conveyance_preference=item.get(
                "webAuthnPolicyPasswordlessAttestationConveyancePreference"
            ),
            web_authn_policy_passwordless_authenticator_attachment=item.get(
                "webAuthnPolicyPasswordlessAuthenticatorAttachment"
            ),
            web_authn_policy_passwordless_avoid_same_authenticator_register=item.get(
                "webAuthnPolicyPasswordlessAvoidSameAuthenticatorRegister"
            ),
            web_authn_policy_passwordless_create_timeout=item.get(
                "webAuthnPolicyPasswordlessCreateTimeout"
            ),
            web_authn_policy_passwordless_require_resident_key=item.get(
                "webAuthnPolicyPasswordlessRequireResidentKey"
            ),
            web_authn_policy_passwordless_rp_entity_name=item.get(
                "webAuthnPolicyPasswordlessRpEntityName"
            ),
            web_authn_policy_passwordless_rp_id=item.get(
                "webAuthnPolicyPasswordlessRpId"
            ),
            web_authn_policy_passwordless_signature_algorithms=item.get(
                "webAuthnPolicyPasswordlessSignatureAlgorithms"
            ),
            web_authn_policy_passwordless_user_verification_requirement=item.get(
                "webAuthnPolicyPasswordlessUserVerificationRequirement"
            ),
            web_authn_policy_require_resident_key=item.get(
                "webAuthnPolicyRequireResidentKey"
            ),
            web_authn_policy_rp_entity_name=item.get("webAuthnPolicyRpEntityName"),
            web_authn_policy_rp_id=item.get("webAuthnPolicyRpId"),
            web_authn_policy_signature_algorithms=item.get(
                "webAuthnPolicySignatureAlgorithms"
            ),
            web_authn_policy_user_verification_requirement=item.get(
                "webAuthnPolicyUserVerificationRequirement"
            ),
        )
