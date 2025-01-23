class RealmRepresentation:
    def __init__(self, access_code_lifespan, access_code_lifespan_login, access_code_lifespan_user_action,
                 access_token_lifespan, access_token_lifespan_for_implicit_flow, account_theme,
                 action_token_generated_by_admin_lifespan, action_token_generated_by_user_lifespan,
                 admin_events_details_enabled, admin_events_enabled, admin_theme, attributes, authentication_flows,
                 authenticator_config, browser_flow, browser_security_headers, brute_force_protected,
                 client_authentication_flow, client_offline_session_idle_timeout, client_offline_session_max_lifespan,
                 client_policies, client_profiles, client_scope_mappings, client_scopes, client_session_idle_timeout,
                 client_session_max_lifespan, clients, components, default_default_client_scopes, default_groups,
                 default_locale, default_optional_client_scopes, default_role, default_signature_algorithm,
                 direct_grant_flow, display_name, display_name_html, docker_authentication_flow,
                 duplicate_emails_allowed, edit_username_allowed, email_theme, enabled, enabled_event_types,
                 events_enabled, events_expiration, events_listeners, failure_factor, federated_users, groups,
                 realm_representation_id, identity_provider_mappers, identity_providers, internationalization_enabled,
                 keycloak_version, login_theme, login_with_email_allowed, max_delta_time_seconds,
                 max_failure_wait_seconds, minimum_quick_login_wait_seconds, not_before, o_auth2_device_code_lifespan,
                 o_auth2_device_polling_interval, oauth2_device_code_lifespan, oauth2_device_polling_interval,
                 offline_session_idle_timeout, offline_session_max_lifespan, offline_session_max_lifespan_enabled,
                 otp_policy_algorithm, otp_policy_digits, otp_policy_initial_counter, otp_policy_look_ahead_window,
                 otp_policy_period, otp_policy_type, otp_supported_applications, password_policy, permanent_lockout,
                 protocol_mappers, quick_login_check_milli_seconds, realm, refresh_token_max_reuse,
                 registration_allowed, registration_email_as_username, registration_flow, remember_me, required_actions,
                 reset_credentials_flow, reset_password_allowed, revoke_refresh_token, roles, scope_mappings,
                 smtp_server, ssl_required, sso_session_idle_timeout, sso_session_idle_timeout_remember_me,
                 sso_session_max_lifespan, sso_session_max_lifespan_remember_me, supported_locales,
                 user_federation_mappers, user_federation_providers, user_managed_access_allowed, users, verify_email,
                 wait_increment_seconds, web_authn_policy_acceptable_aaguids,
                 web_authn_policy_attestation_conveyance_preference, web_authn_policy_authenticator_attachment,
                 web_authn_policy_avoid_same_authenticator_register, web_authn_policy_create_timeout,
                 web_authn_policy_passwordless_acceptable_aaguids,
                 web_authn_policy_passwordless_attestation_conveyance_preference,
                 web_authn_policy_passwordless_authenticator_attachment,
                 web_authn_policy_passwordless_avoid_same_authenticator_register,
                 web_authn_policy_passwordless_create_timeout, web_authn_policy_passwordless_require_resident_key,
                 web_authn_policy_passwordless_rp_entity_name, web_authn_policy_passwordless_rp_id,
                 web_authn_policy_passwordless_signature_algorithms,
                 web_authn_policy_passwordless_user_verification_requirement, web_authn_policy_require_resident_key,
                 web_authn_policy_rp_entity_name, web_authn_policy_rp_id, web_authn_policy_signature_algorithms,
                 web_authn_policy_user_verification_requirement):
        self.accessCodeLifespan = access_code_lifespan
        self.accessCodeLifespanLogin = access_code_lifespan_login
        self.accessCodeLifespanUserAction = access_code_lifespan_user_action
        self.accessTokenLifespan = access_token_lifespan
        self.accessTokenLifespanForImplicitFlow = access_token_lifespan_for_implicit_flow
        self.accountTheme = account_theme
        self.actionTokenGeneratedByAdminLifespan = action_token_generated_by_admin_lifespan
        self.actionTokenGeneratedByUserLifespan = action_token_generated_by_user_lifespan
        self.adminEventsDetailsEnabled = admin_events_details_enabled
        self.adminEventsEnabled = admin_events_enabled
        self.adminTheme = admin_theme
        self.attributes = attributes
        self.authenticationFlows = authentication_flows
        self.authenticatorConfig = authenticator_config
        self.browserFlow = browser_flow
        self.browserSecurityHeaders = browser_security_headers
        self.bruteForceProtected = brute_force_protected
        self.clientAuthenticationFlow = client_authentication_flow
        self.clientOfflineSessionIdleTimeout = client_offline_session_idle_timeout
        self.clientOfflineSessionMaxLifespan = client_offline_session_max_lifespan
        self.clientPolicies = client_policies
        self.clientProfiles = client_profiles
        self.clientScopeMappings = client_scope_mappings
        self.clientScopes = client_scopes
        self.clientSessionIdleTimeout = client_session_idle_timeout
        self.clientSessionMaxLifespan = client_session_max_lifespan
        self.clients = clients
        self.components = components
        self.defaultDefaultClientScopes = default_default_client_scopes
        self.defaultGroups = default_groups
        self.defaultLocale = default_locale
        self.defaultOptionalClientScopes = default_optional_client_scopes
        self.defaultRole = default_role
        self.defaultSignatureAlgorithm = default_signature_algorithm
        self.directGrantFlow = direct_grant_flow
        self.displayName = display_name
        self.displayNameHtml = display_name_html
        self.dockerAuthenticationFlow = docker_authentication_flow
        self.duplicateEmailsAllowed = duplicate_emails_allowed
        self.editUsernameAllowed = edit_username_allowed
        self.emailTheme = email_theme
        self.enabled = enabled
        self.enabledEventTypes = enabled_event_types
        self.eventsEnabled = events_enabled
        self.eventsExpiration = events_expiration
        self.eventsListeners = events_listeners
        self.failureFactor = failure_factor
        self.federatedUsers = federated_users
        self.groups = groups
        self.id = realm_representation_id
        self.identityProviderMappers = identity_provider_mappers
        self.identityProviders = identity_providers
        self.internationalizationEnabled = internationalization_enabled
        self.keycloakVersion = keycloak_version
        self.loginTheme = login_theme
        self.loginWithEmailAllowed = login_with_email_allowed
        self.maxDeltaTimeSeconds = max_delta_time_seconds
        self.maxFailureWaitSeconds = max_failure_wait_seconds
        self.minimumQuickLoginWaitSeconds = minimum_quick_login_wait_seconds
        self.notBefore = not_before
        self.oAuth2DeviceCodeLifespan = o_auth2_device_code_lifespan
        self.oAuth2DevicePollingInterval = o_auth2_device_polling_interval
        self.oauth2DeviceCodeLifespan = oauth2_device_code_lifespan
        self.oauth2DevicePollingInterval = oauth2_device_polling_interval
        self.offlineSessionIdleTimeout = offline_session_idle_timeout
        self.offlineSessionMaxLifespan = offline_session_max_lifespan
        self.offlineSessionMaxLifespanEnabled = offline_session_max_lifespan_enabled
        self.otpPolicyAlgorithm = otp_policy_algorithm
        self.otpPolicyDigits = otp_policy_digits
        self.otpPolicyInitialCounter = otp_policy_initial_counter
        self.otpPolicyLookAheadWindow = otp_policy_look_ahead_window
        self.otpPolicyPeriod = otp_policy_period
        self.otpPolicyType = otp_policy_type
        self.otpSupportedApplications = otp_supported_applications
        self.passwordPolicy = password_policy
        self.permanentLockout = permanent_lockout
        self.protocolMappers = protocol_mappers
        self.quickLoginCheckMilliSeconds = quick_login_check_milli_seconds
        self.realm = realm
        self.refreshTokenMaxReuse = refresh_token_max_reuse
        self.registrationAllowed = registration_allowed
        self.registrationEmailAsUsername = registration_email_as_username
        self.registrationFlow = registration_flow
        self.rememberMe = remember_me
        self.requiredActions = required_actions
        self.resetCredentialsFlow = reset_credentials_flow
        self.resetPasswordAllowed = reset_password_allowed
        self.revokeRefreshToken = revoke_refresh_token
        self.roles = roles
        self.scopeMappings = scope_mappings
        self.smtpServer = smtp_server
        self.sslRequired = ssl_required
        self.ssoSessionIdleTimeout = sso_session_idle_timeout
        self.ssoSessionIdleTimeoutRememberMe = sso_session_idle_timeout_remember_me
        self.ssoSessionMaxLifespan = sso_session_max_lifespan
        self.ssoSessionMaxLifespanRememberMe = sso_session_max_lifespan_remember_me
        self.supportedLocales = supported_locales
        self.userFederationMappers = user_federation_mappers
        self.userFederationProviders = user_federation_providers
        self.userManagedAccessAllowed = user_managed_access_allowed
        self.users = users
        self.verifyEmail = verify_email
        self.waitIncrementSeconds = wait_increment_seconds
        self.webAuthnPolicyAcceptableAaguids = web_authn_policy_acceptable_aaguids
        self.webAuthnPolicyAttestationConveyancePreference = web_authn_policy_attestation_conveyance_preference
        self.webAuthnPolicyAuthenticatorAttachment = web_authn_policy_authenticator_attachment
        self.webAuthnPolicyAvoidSameAuthenticatorRegister = web_authn_policy_avoid_same_authenticator_register
        self.webAuthnPolicyCreateTimeout = web_authn_policy_create_timeout
        self.webAuthnPolicyPasswordlessAcceptableAaguids = web_authn_policy_passwordless_acceptable_aaguids
        self.webAuthnPolicyPasswordlessAttestationConveyancePreference = web_authn_policy_passwordless_attestation_conveyance_preference
        self.webAuthnPolicyPasswordlessAuthenticatorAttachment = web_authn_policy_passwordless_authenticator_attachment
        self.webAuthnPolicyPasswordlessAvoidSameAuthenticatorRegister = web_authn_policy_passwordless_avoid_same_authenticator_register
        self.webAuthnPolicyPasswordlessCreateTimeout = web_authn_policy_passwordless_create_timeout
        self.webAuthnPolicyPasswordlessRequireResidentKey = web_authn_policy_passwordless_require_resident_key
        self.webAuthnPolicyPasswordlessRpEntityName = web_authn_policy_passwordless_rp_entity_name
        self.webAuthnPolicyPasswordlessRpId = web_authn_policy_passwordless_rp_id
        self.webAuthnPolicyPasswordlessSignatureAlgorithms = web_authn_policy_passwordless_signature_algorithms
        self.webAuthnPolicyPasswordlessUserVerificationRequirement = web_authn_policy_passwordless_user_verification_requirement
        self.webAuthnPolicyRequireResidentKey = web_authn_policy_require_resident_key
        self.webAuthnPolicyRpEntityName = web_authn_policy_rp_entity_name
        self.webAuthnPolicyRpId = web_authn_policy_rp_id
        self.webAuthnPolicySignatureAlgorithms = web_authn_policy_signature_algorithms
        self.webAuthnPolicyUserVerificationRequirement = web_authn_policy_user_verification_requirement

    def __str__(self):
        return f"RealmRepresentation(" \
               f"accessCodeLifespan={self.accessCodeLifespan} " \
               f"accessCodeLifespanLogin={self.accessCodeLifespanLogin} " \
               f"accessCodeLifespanUserAction={self.accessCodeLifespanUserAction} " \
               f"accessTokenLifespan={self.accessTokenLifespan} " \
               f"accessTokenLifespanForImplicitFlow={self.accessTokenLifespanForImplicitFlow} " \
               f"accountTheme={self.accountTheme} " \
               f"actionTokenGeneratedByAdminLifespan={self.actionTokenGeneratedByAdminLifespan} " \
               f"actionTokenGeneratedByUserLifespan={self.actionTokenGeneratedByUserLifespan} " \
               f"adminEventsDetailsEnabled={self.adminEventsDetailsEnabled} " \
               f"adminEventsEnabled={self.adminEventsEnabled} " \
               f"adminTheme={self.adminTheme} " \
               f"attributes={self.attributes} " \
               f"authenticationFlows={self.authenticationFlows} " \
               f"authenticatorConfig={self.authenticatorConfig} " \
               f"browserFlow={self.browserFlow} " \
               f"browserSecurityHeaders={self.browserSecurityHeaders} " \
               f"bruteForceProtected={self.bruteForceProtected} " \
               f"clientAuthenticationFlow={self.clientAuthenticationFlow} " \
               f"clientOfflineSessionIdleTimeout={self.clientOfflineSessionIdleTimeout} " \
               f"clientOfflineSessionMaxLifespan={self.clientOfflineSessionMaxLifespan} " \
               f"clientPolicies={self.clientPolicies} " \
               f"clientProfiles={self.clientProfiles} " \
               f"clientScopeMappings={self.clientScopeMappings} " \
               f"clientScopes={self.clientScopes} " \
               f"clientSessionIdleTimeout={self.clientSessionIdleTimeout} " \
               f"clientSessionMaxLifespan={self.clientSessionMaxLifespan} " \
               f"clients={self.clients} " \
               f"components={self.components} " \
               f"defaultDefaultClientScopes={self.defaultDefaultClientScopes} " \
               f"defaultGroups={self.defaultGroups} " \
               f"defaultLocale={self.defaultLocale} " \
               f"defaultOptionalClientScopes={self.defaultOptionalClientScopes} " \
               f"defaultRole={self.defaultRole} " \
               f"defaultSignatureAlgorithm={self.defaultSignatureAlgorithm} " \
               f"directGrantFlow={self.directGrantFlow} " \
               f"displayName={self.displayName} " \
               f"displayNameHtml={self.displayNameHtml} " \
               f"dockerAuthenticationFlow={self.dockerAuthenticationFlow} " \
               f"duplicateEmailsAllowed={self.duplicateEmailsAllowed} " \
               f"editUsernameAllowed={self.editUsernameAllowed} " \
               f"emailTheme={self.emailTheme} " \
               f"enabled={self.enabled} " \
               f"enabledEventTypes={self.enabledEventTypes} " \
               f"eventsEnabled={self.eventsEnabled} " \
               f"eventsExpiration={self.eventsExpiration} " \
               f"eventsListeners={self.eventsListeners} " \
               f"failureFactor={self.failureFactor} " \
               f"federatedUsers={self.federatedUsers} " \
               f"groups={self.groups} " \
               f"id={self.id} " \
               f"identityProviderMappers={self.identityProviderMappers} " \
               f"identityProviders={self.identityProviders} " \
               f"internationalizationEnabled={self.internationalizationEnabled} " \
               f"keycloakVersion={self.keycloakVersion} " \
               f"loginTheme={self.loginTheme} " \
               f"loginWithEmailAllowed={self.loginWithEmailAllowed} " \
               f"maxDeltaTimeSeconds={self.maxDeltaTimeSeconds} " \
               f"maxFailureWaitSeconds={self.maxFailureWaitSeconds} " \
               f"minimumQuickLoginWaitSeconds={self.minimumQuickLoginWaitSeconds} " \
               f"notBefore={self.notBefore} " \
               f"oAuth2DeviceCodeLifespan={self.oAuth2DeviceCodeLifespan} " \
               f"oAuth2DevicePollingInterval={self.oAuth2DevicePollingInterval} " \
               f"oauth2DeviceCodeLifespan={self.oauth2DeviceCodeLifespan} " \
               f"oauth2DevicePollingInterval={self.oauth2DevicePollingInterval} " \
               f"offlineSessionIdleTimeout={self.offlineSessionIdleTimeout} " \
               f"offlineSessionMaxLifespan={self.offlineSessionMaxLifespan} " \
               f"offlineSessionMaxLifespanEnabled={self.offlineSessionMaxLifespanEnabled} " \
               f"otpPolicyAlgorithm={self.otpPolicyAlgorithm} " \
               f"otpPolicyDigits={self.otpPolicyDigits} " \
               f"otpPolicyInitialCounter={self.otpPolicyInitialCounter} " \
               f"otpPolicyLookAheadWindow={self.otpPolicyLookAheadWindow} " \
               f"otpPolicyPeriod={self.otpPolicyPeriod} " \
               f"otpPolicyType={self.otpPolicyType} " \
               f"otpSupportedApplications={self.otpSupportedApplications} " \
               f"passwordPolicy={self.passwordPolicy} " \
               f"permanentLockout={self.permanentLockout} " \
               f"protocolMappers={self.protocolMappers} " \
               f"quickLoginCheckMilliSeconds={self.quickLoginCheckMilliSeconds} " \
               f"realm={self.realm} " \
               f"refreshTokenMaxReuse={self.refreshTokenMaxReuse} " \
               f"registrationAllowed={self.registrationAllowed} " \
               f"registrationEmailAsUsername={self.registrationEmailAsUsername} " \
               f"registrationFlow={self.registrationFlow} " \
               f"rememberMe={self.rememberMe} " \
               f"requiredActions={self.requiredActions} " \
               f"resetCredentialsFlow={self.resetCredentialsFlow} " \
               f"resetPasswordAllowed={self.resetPasswordAllowed} " \
               f"revokeRefreshToken={self.revokeRefreshToken} " \
               f"roles={self.roles} " \
               f"scopeMappings={self.scopeMappings} " \
               f"smtpServer={self.smtpServer} " \
               f"sslRequired={self.sslRequired} " \
               f"ssoSessionIdleTimeout={self.ssoSessionIdleTimeout} " \
               f"ssoSessionIdleTimeoutRememberMe={self.ssoSessionIdleTimeoutRememberMe} " \
               f"ssoSessionMaxLifespan={self.ssoSessionMaxLifespan} " \
               f"ssoSessionMaxLifespanRememberMe={self.ssoSessionMaxLifespanRememberMe} " \
               f"supportedLocales={self.supportedLocales} " \
               f"userFederationMappers={self.userFederationMappers} " \
               f"userFederationProviders={self.userFederationProviders} " \
               f"userManagedAccessAllowed={self.userManagedAccessAllowed} " \
               f"users={self.users} " \
               f"verifyEmail={self.verifyEmail} " \
               f"waitIncrementSeconds={self.waitIncrementSeconds} " \
               f"webAuthnPolicyAcceptableAaguids={self.webAuthnPolicyAcceptableAaguids} " \
               f"webAuthnPolicyAttestationConveyancePreference={self.webAuthnPolicyAttestationConveyancePreference} " \
               f"webAuthnPolicyAuthenticatorAttachment={self.webAuthnPolicyAuthenticatorAttachment} " \
               f"webAuthnPolicyAvoidSameAuthenticatorRegister={self.webAuthnPolicyAvoidSameAuthenticatorRegister} " \
               f"webAuthnPolicyCreateTimeout={self.webAuthnPolicyCreateTimeout} " \
               f"webAuthnPolicyPasswordlessAcceptableAaguids={self.webAuthnPolicyPasswordlessAcceptableAaguids} " \
               f"webAuthnPolicyPasswordlessAttestationConveyancePreference={self.webAuthnPolicyPasswordlessAttestationConveyancePreference} " \
               f"webAuthnPolicyPasswordlessAuthenticatorAttachment={self.webAuthnPolicyPasswordlessAuthenticatorAttachment} " \
               f"webAuthnPolicyPasswordlessAvoidSameAuthenticatorRegister={self.webAuthnPolicyPasswordlessAvoidSameAuthenticatorRegister} " \
               f"webAuthnPolicyPasswordlessCreateTimeout={self.webAuthnPolicyPasswordlessCreateTimeout} " \
               f"webAuthnPolicyPasswordlessRequireResidentKey={self.webAuthnPolicyPasswordlessRequireResidentKey} " \
               f"webAuthnPolicyPasswordlessRpEntityName={self.webAuthnPolicyPasswordlessRpEntityName} " \
               f"webAuthnPolicyPasswordlessRpId={self.webAuthnPolicyPasswordlessRpId} " \
               f"webAuthnPolicyPasswordlessSignatureAlgorithms={self.webAuthnPolicyPasswordlessSignatureAlgorithms} " \
               f"webAuthnPolicyPasswordlessUserVerificationRequirement={self.webAuthnPolicyPasswordlessUserVerificationRequirement} " \
               f"webAuthnPolicyRequireResidentKey={self.webAuthnPolicyRequireResidentKey} " \
               f"webAuthnPolicyRpEntityName={self.webAuthnPolicyRpEntityName} " \
               f"webAuthnPolicyRpId={self.webAuthnPolicyRpId} " \
               f"webAuthnPolicySignatureAlgorithms={self.webAuthnPolicySignatureAlgorithms} " \
               f"webAuthnPolicyUserVerificationRequirement={self.webAuthnPolicyUserVerificationRequirement} " \
               f")"

    def to_dict(self):
        return {
            "accessCodeLifespan": self.accessCodeLifespan,
            "accessCodeLifespanLogin": self.accessCodeLifespanLogin,
            "accessCodeLifespanUserAction": self.accessCodeLifespanUserAction,
            "accessTokenLifespan": self.accessTokenLifespan,
            "accessTokenLifespanForImplicitFlow": self.accessTokenLifespanForImplicitFlow,
            "accountTheme": self.accountTheme,
            "actionTokenGeneratedByAdminLifespan": self.actionTokenGeneratedByAdminLifespan,
            "actionTokenGeneratedByUserLifespan": self.actionTokenGeneratedByUserLifespan,
            "adminEventsDetailsEnabled": self.adminEventsDetailsEnabled,
            "adminEventsEnabled": self.adminEventsEnabled,
            "adminTheme": self.adminTheme,
            "attributes": self.attributes,
            "authenticationFlows": self.authenticationFlows,
            "authenticatorConfig": self.authenticatorConfig,
            "browserFlow": self.browserFlow,
            "browserSecurityHeaders": self.browserSecurityHeaders,
            "bruteForceProtected": self.bruteForceProtected,
            "clientAuthenticationFlow": self.clientAuthenticationFlow,
            "clientOfflineSessionIdleTimeout": self.clientOfflineSessionIdleTimeout,
            "clientOfflineSessionMaxLifespan": self.clientOfflineSessionMaxLifespan,
            "clientPolicies": self.clientPolicies,
            "clientProfiles": self.clientProfiles,
            "clientScopeMappings": self.clientScopeMappings,
            "clientScopes": self.clientScopes,
            "clientSessionIdleTimeout": self.clientSessionIdleTimeout,
            "clientSessionMaxLifespan": self.clientSessionMaxLifespan,
            "clients": self.clients,
            "components": self.components,
            "defaultDefaultClientScopes": self.defaultDefaultClientScopes,
            "defaultGroups": self.defaultGroups,
            "defaultLocale": self.defaultLocale,
            "defaultOptionalClientScopes": self.defaultOptionalClientScopes,
            "defaultRole": self.defaultRole,
            "defaultSignatureAlgorithm": self.defaultSignatureAlgorithm,
            "directGrantFlow": self.directGrantFlow,
            "displayName": self.displayName,
            "displayNameHtml": self.displayNameHtml,
            "dockerAuthenticationFlow": self.dockerAuthenticationFlow,
            "duplicateEmailsAllowed": self.duplicateEmailsAllowed,
            "editUsernameAllowed": self.editUsernameAllowed,
            "emailTheme": self.emailTheme,
            "enabled": self.enabled,
            "enabledEventTypes": self.enabledEventTypes,
            "eventsEnabled": self.eventsEnabled,
            "eventsExpiration": self.eventsExpiration,
            "eventsListeners": self.eventsListeners,
            "failureFactor": self.failureFactor,
            "federatedUsers": self.federatedUsers,
            "groups": self.groups,
            "id": self.id,
            "identityProviderMappers": self.identityProviderMappers,
            "identityProviders": self.identityProviders,
            "internationalizationEnabled": self.internationalizationEnabled,
            "keycloakVersion": self.keycloakVersion,
            "loginTheme": self.loginTheme,
            "loginWithEmailAllowed": self.loginWithEmailAllowed,
            "maxDeltaTimeSeconds": self.maxDeltaTimeSeconds,
            "maxFailureWaitSeconds": self.maxFailureWaitSeconds,
            "minimumQuickLoginWaitSeconds": self.minimumQuickLoginWaitSeconds,
            "notBefore": self.notBefore,
            "oAuth2DeviceCodeLifespan": self.oAuth2DeviceCodeLifespan,
            "oAuth2DevicePollingInterval": self.oAuth2DevicePollingInterval,
            "oauth2DeviceCodeLifespan": self.oauth2DeviceCodeLifespan,
            "oauth2DevicePollingInterval": self.oauth2DevicePollingInterval,
            "offlineSessionIdleTimeout": self.offlineSessionIdleTimeout,
            "offlineSessionMaxLifespan": self.offlineSessionMaxLifespan,
            "offlineSessionMaxLifespanEnabled": self.offlineSessionMaxLifespanEnabled,
            "otpPolicyAlgorithm": self.otpPolicyAlgorithm,
            "otpPolicyDigits": self.otpPolicyDigits,
            "otpPolicyInitialCounter": self.otpPolicyInitialCounter,
            "otpPolicyLookAheadWindow": self.otpPolicyLookAheadWindow,
            "otpPolicyPeriod": self.otpPolicyPeriod,
            "otpPolicyType": self.otpPolicyType,
            "otpSupportedApplications": self.otpSupportedApplications,
            "passwordPolicy": self.passwordPolicy,
            "permanentLockout": self.permanentLockout,
            "protocolMappers": self.protocolMappers,
            "quickLoginCheckMilliSeconds": self.quickLoginCheckMilliSeconds,
            "realm": self.realm,
            "refreshTokenMaxReuse": self.refreshTokenMaxReuse,
            "registrationAllowed": self.registrationAllowed,
            "registrationEmailAsUsername": self.registrationEmailAsUsername,
            "registrationFlow": self.registrationFlow,
            "rememberMe": self.rememberMe,
            "requiredActions": self.requiredActions,
            "resetCredentialsFlow": self.resetCredentialsFlow,
            "resetPasswordAllowed": self.resetPasswordAllowed,
            "revokeRefreshToken": self.revokeRefreshToken,
            "roles": self.roles,
            "scopeMappings": self.scopeMappings,
            "smtpServer": self.smtpServer,
            "sslRequired": self.sslRequired,
            "ssoSessionIdleTimeout": self.ssoSessionIdleTimeout,
            "ssoSessionIdleTimeoutRememberMe": self.ssoSessionIdleTimeoutRememberMe,
            "ssoSessionMaxLifespan": self.ssoSessionMaxLifespan,
            "ssoSessionMaxLifespanRememberMe": self.ssoSessionMaxLifespanRememberMe,
            "supportedLocales": self.supportedLocales,
            "userFederationMappers": self.userFederationMappers,
            "userFederationProviders": self.userFederationProviders,
            "userManagedAccessAllowed": self.userManagedAccessAllowed,
            "users": self.users,
            "verifyEmail": self.verifyEmail,
            "waitIncrementSeconds": self.waitIncrementSeconds,
            "webAuthnPolicyAcceptableAaguids": self.webAuthnPolicyAcceptableAaguids,
            "webAuthnPolicyAttestationConveyancePreference": self.webAuthnPolicyAttestationConveyancePreference,
            "webAuthnPolicyAuthenticatorAttachment": self.webAuthnPolicyAuthenticatorAttachment,
            "webAuthnPolicyAvoidSameAuthenticatorRegister": self.webAuthnPolicyAvoidSameAuthenticatorRegister,
            "webAuthnPolicyCreateTimeout": self.webAuthnPolicyCreateTimeout,
            "webAuthnPolicyPasswordlessAcceptableAaguids": self.webAuthnPolicyPasswordlessAcceptableAaguids,
            "webAuthnPolicyPasswordlessAttestationConveyancePreference": self.webAuthnPolicyPasswordlessAttestationConveyancePreference,
            "webAuthnPolicyPasswordlessAuthenticatorAttachment": self.webAuthnPolicyPasswordlessAuthenticatorAttachment,
            "webAuthnPolicyPasswordlessAvoidSameAuthenticatorRegister": self.webAuthnPolicyPasswordlessAvoidSameAuthenticatorRegister,
            "webAuthnPolicyPasswordlessCreateTimeout": self.webAuthnPolicyPasswordlessCreateTimeout,
            "webAuthnPolicyPasswordlessRequireResidentKey": self.webAuthnPolicyPasswordlessRequireResidentKey,
            "webAuthnPolicyPasswordlessRpEntityName": self.webAuthnPolicyPasswordlessRpEntityName,
            "webAuthnPolicyPasswordlessRpId": self.webAuthnPolicyPasswordlessRpId,
            "webAuthnPolicyPasswordlessSignatureAlgorithms": self.webAuthnPolicyPasswordlessSignatureAlgorithms,
            "webAuthnPolicyPasswordlessUserVerificationRequirement": self.webAuthnPolicyPasswordlessUserVerificationRequirement,
            "webAuthnPolicyRequireResidentKey": self.webAuthnPolicyRequireResidentKey,
            "webAuthnPolicyRpEntityName": self.webAuthnPolicyRpEntityName,
            "webAuthnPolicyRpId": self.webAuthnPolicyRpId,
            "webAuthnPolicySignatureAlgorithms": self.webAuthnPolicySignatureAlgorithms,
            "webAuthnPolicyUserVerificationRequirement": self.webAuthnPolicyUserVerificationRequirement,
        }


def construct_realm_representation(item):
    return RealmRepresentation(
        access_code_lifespan=item.get("accessCodeLifespan"),
        access_code_lifespan_login=item.get("accessCodeLifespanLogin"),
        access_code_lifespan_user_action=item.get("accessCodeLifespanUserAction"),
        access_token_lifespan=item.get("accessTokenLifespan"),
        access_token_lifespan_for_implicit_flow=item.get("accessTokenLifespanForImplicitFlow"),
        account_theme=item.get("accountTheme"),
        action_token_generated_by_admin_lifespan=item.get("actionTokenGeneratedByAdminLifespan"),
        action_token_generated_by_user_lifespan=item.get("actionTokenGeneratedByUserLifespan"),
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
        client_offline_session_idle_timeout=item.get("clientOfflineSessionIdleTimeout"),
        client_offline_session_max_lifespan=item.get("clientOfflineSessionMaxLifespan"),
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
        offline_session_max_lifespan_enabled=item.get("offlineSessionMaxLifespanEnabled"),
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
        sso_session_idle_timeout_remember_me=item.get("ssoSessionIdleTimeoutRememberMe"),
        sso_session_max_lifespan=item.get("ssoSessionMaxLifespan"),
        sso_session_max_lifespan_remember_me=item.get("ssoSessionMaxLifespanRememberMe"),
        supported_locales=item.get("supportedLocales"),
        user_federation_mappers=item.get("userFederationMappers"),
        user_federation_providers=item.get("userFederationProviders"),
        user_managed_access_allowed=item.get("userManagedAccessAllowed"),
        users=item.get("users"),
        verify_email=item.get("verifyEmail"),
        wait_increment_seconds=item.get("waitIncrementSeconds"),
        web_authn_policy_acceptable_aaguids=item.get("webAuthnPolicyAcceptableAaguids"),
        web_authn_policy_attestation_conveyance_preference=item.get("webAuthnPolicyAttestationConveyancePreference"),
        web_authn_policy_authenticator_attachment=item.get("webAuthnPolicyAuthenticatorAttachment"),
        web_authn_policy_avoid_same_authenticator_register=item.get("webAuthnPolicyAvoidSameAuthenticatorRegister"),
        web_authn_policy_create_timeout=item.get("webAuthnPolicyCreateTimeout"),
        web_authn_policy_passwordless_acceptable_aaguids=item.get("webAuthnPolicyPasswordlessAcceptableAaguids"),
        web_authn_policy_passwordless_attestation_conveyance_preference=item.get(
            "webAuthnPolicyPasswordlessAttestationConveyancePreference"),
        web_authn_policy_passwordless_authenticator_attachment=item.get(
            "webAuthnPolicyPasswordlessAuthenticatorAttachment"),
        web_authn_policy_passwordless_avoid_same_authenticator_register=item.get(
            "webAuthnPolicyPasswordlessAvoidSameAuthenticatorRegister"),
        web_authn_policy_passwordless_create_timeout=item.get("webAuthnPolicyPasswordlessCreateTimeout"),
        web_authn_policy_passwordless_require_resident_key=item.get("webAuthnPolicyPasswordlessRequireResidentKey"),
        web_authn_policy_passwordless_rp_entity_name=item.get("webAuthnPolicyPasswordlessRpEntityName"),
        web_authn_policy_passwordless_rp_id=item.get("webAuthnPolicyPasswordlessRpId"),
        web_authn_policy_passwordless_signature_algorithms=item.get("webAuthnPolicyPasswordlessSignatureAlgorithms"),
        web_authn_policy_passwordless_user_verification_requirement=item.get(
            "webAuthnPolicyPasswordlessUserVerificationRequirement"),
        web_authn_policy_require_resident_key=item.get("webAuthnPolicyRequireResidentKey"),
        web_authn_policy_rp_entity_name=item.get("webAuthnPolicyRpEntityName"),
        web_authn_policy_rp_id=item.get("webAuthnPolicyRpId"),
        web_authn_policy_signature_algorithms=item.get("webAuthnPolicySignatureAlgorithms"),
        web_authn_policy_user_verification_requirement=item.get("webAuthnPolicyUserVerificationRequirement"),
    )
