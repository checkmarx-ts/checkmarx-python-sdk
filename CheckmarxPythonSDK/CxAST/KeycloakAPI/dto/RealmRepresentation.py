import json


class RealmRepresentation(object):
    def __init__(self, realm_id, realm, display_name, not_before, revoke_refresh_token, refresh_token_max_reuse,
                 access_token_lifespan, access_token_lifespan_for_implicit_flow, sso_session_idle_timeout,
                 sso_session_max_lifespan, sso_session_idle_timeout_remember_me, sso_session_max_lifespan_remember_me,
                 offline_session_idle_timeout, offline_session_max_lifespan_enabled, offline_session_max_lifespan,
                 client_session_idle_timeout, client_session_max_lifespan, client_offline_session_idle_timeout,
                 client_offline_session_max_lifespan, access_code_lifespan, access_code_lifespan_user_action,
                 access_code_lifespan_login, action_token_generated_by_admin_lifespan,
                 action_token_generated_by_user_lifespan, oauth_2_device_code_lifespan, oauth_2_device_polling_interval,
                 enabled, ssl_required, registration_allowed, registration_email_as_username, remember_me, verify_email,
                 login_with_email_allowed, duplicate_emails_allowed, reset_password_allowed, edit_username_allowed,
                 brute_force_protected, permanent_lockout, max_failure_wait_seconds, minimum_quick_login_wait_seconds,
                 wait_increment_seconds, quick_login_check_milli_seconds, max_delta_time_seconds, failure_factor,
                 default_role, required_credentials, password_policy, otp_policy_type, otp_policy_algorithm,
                 otp_policy_initial_counter, otp_policy_digits, otp_policy_look_ahead_window, otp_policy_period,
                 otp_supported_applications, web_authn_policy_rp_entity_name, web_authn_policy_signature_algorithms,
                 web_authn_policy_rp_id, web_authn_policy_attestation_conveyance_preference,
                 web_authn_policy_authenticator_attachment, web_authn_policy_require_resident_key,
                 web_authn_policy_user_verification_requirement, web_authn_policy_create_timeout,
                 web_authn_policy_avoid_same_authenticator_register, web_authn_policy_acceptable_aaguids,
                 web_authn_policy_passwordless_rp_entity_name, web_authn_policy_passwordless_signature_algorithms,
                 web_authn_policy_passwordless_rp_id, web_authn_policy_passwordless_attestation_conveyance_preference,
                 web_authn_policy_passwordless_authenticator_attachment,
                 web_authn_policy_passwordless_require_resident_key,
                 web_authn_policy_passwordless_user_verification_requirement,
                 web_authn_policy_passwordless_create_timeout,
                 web_authn_policy_passwordless_avoid_same_authenticator_register,
                 web_authn_policy_passwordless_acceptable_aaguids, browser_security_headers, smtp_server, login_theme,
                 account_theme, admin_theme, email_theme, events_enabled, events_expiration, events_listeners,
                 enabled_event_types, admin_events_enabled, admin_events_details_enabled, identity_providers,
                 identity_provider_mappers, internationalization_enabled, supported_locales, browser_flow,
                 registration_flow, direct_grant_flow, reset_credentials_flow, client_authentication_flow,
                 docker_authentication_flow, attributes, user_managed_access_allowed, client_profiles, client_policies):
        self.id = realm_id
        self.realm = realm
        self.displayName = display_name
        self.notBefore = not_before
        self.revokeRefreshToken = revoke_refresh_token
        self.refreshTokenMaxReuse = refresh_token_max_reuse
        self.accessTokenLifespan = access_token_lifespan
        self.accessTokenLifespanForImplicitFlow = access_token_lifespan_for_implicit_flow
        self.ssoSessionIdleTimeout = sso_session_idle_timeout
        self.ssoSessionMaxLifespan = sso_session_max_lifespan
        self.ssoSessionIdleTimeoutRememberMe = sso_session_idle_timeout_remember_me
        self.ssoSessionMaxLifespanRememberMe = sso_session_max_lifespan_remember_me
        self.offlineSessionIdleTimeout = offline_session_idle_timeout
        self.offlineSessionMaxLifespanEnabled = offline_session_max_lifespan_enabled
        self.offlineSessionMaxLifespan = offline_session_max_lifespan
        self.clientSessionIdleTimeout = client_session_idle_timeout
        self.clientSessionMaxLifespan = client_session_max_lifespan
        self.clientOfflineSessionIdleTimeout = client_offline_session_idle_timeout
        self.clientOfflineSessionMaxLifespan = client_offline_session_max_lifespan
        self.accessCodeLifespan = access_code_lifespan
        self.accessCodeLifespanUserAction = access_code_lifespan_user_action
        self.accessCodeLifespanLogin = access_code_lifespan_login
        self.actionTokenGeneratedByAdminLifespan = action_token_generated_by_admin_lifespan
        self.actionTokenGeneratedByUserLifespan = action_token_generated_by_user_lifespan
        self.oauth2DeviceCodeLifespan = oauth_2_device_code_lifespan
        self.oauth2DevicePollingInterval = oauth_2_device_polling_interval
        self.enabled = enabled
        self.sslRequired = ssl_required
        self.registrationAllowed = registration_allowed
        self.registrationEmailAsUsername = registration_email_as_username
        self.rememberMe = remember_me
        self.verifyEmail = verify_email
        self.loginWithEmailAllowed = login_with_email_allowed
        self.duplicateEmailsAllowed = duplicate_emails_allowed
        self.resetPasswordAllowed = reset_password_allowed
        self.editUsernameAllowed = edit_username_allowed
        self.bruteForceProtected = brute_force_protected
        self.permanentLockout = permanent_lockout
        self.maxFailureWaitSeconds = max_failure_wait_seconds
        self.minimumQuickLoginWaitSeconds = minimum_quick_login_wait_seconds
        self.waitIncrementSeconds = wait_increment_seconds
        self.quickLoginCheckMilliSeconds = quick_login_check_milli_seconds
        self.maxDeltaTimeSeconds = max_delta_time_seconds
        self.failureFactor = failure_factor
        self.defaultRole = default_role
        self.requiredCredentials = required_credentials
        self.passwordPolicy = password_policy
        self.otpPolicyType = otp_policy_type
        self.otpPolicyAlgorithm = otp_policy_algorithm
        self.otpPolicyInitialCounter = otp_policy_initial_counter
        self.otpPolicyDigits = otp_policy_digits
        self.otpPolicyLookAheadWindow = otp_policy_look_ahead_window
        self.otpPolicyPeriod = otp_policy_period
        self.otpSupportedApplications = otp_supported_applications
        self.webAuthnPolicyRpEntityName = web_authn_policy_rp_entity_name
        self.webAuthnPolicySignatureAlgorithms = web_authn_policy_signature_algorithms
        self.webAuthnPolicyRpId = web_authn_policy_rp_id
        self.webAuthnPolicyAttestationConveyancePreference = web_authn_policy_attestation_conveyance_preference
        self.webAuthnPolicyAuthenticatorAttachment = web_authn_policy_authenticator_attachment
        self.webAuthnPolicyRequireResidentKey = web_authn_policy_require_resident_key
        self.webAuthnPolicyUserVerificationRequirement = web_authn_policy_user_verification_requirement
        self.webAuthnPolicyCreateTimeout = web_authn_policy_create_timeout
        self.webAuthnPolicyAvoidSameAuthenticatorRegister = web_authn_policy_avoid_same_authenticator_register
        self.webAuthnPolicyAcceptableAaguids = web_authn_policy_acceptable_aaguids
        self.webAuthnPolicyPasswordlessRpEntityName = web_authn_policy_passwordless_rp_entity_name
        self.webAuthnPolicyPasswordlessSignatureAlgorithms = web_authn_policy_passwordless_signature_algorithms
        self.webAuthnPolicyPasswordlessRpId = web_authn_policy_passwordless_rp_id
        self.webAuthnPolicyPasswordlessAttestationConveyancePreference \
            = web_authn_policy_passwordless_attestation_conveyance_preference
        self.webAuthnPolicyPasswordlessAuthenticatorAttachment = web_authn_policy_passwordless_authenticator_attachment
        self.webAuthnPolicyPasswordlessRequireResidentKey = web_authn_policy_passwordless_require_resident_key
        self.webAuthnPolicyPasswordlessUserVerificationRequirement \
            = web_authn_policy_passwordless_user_verification_requirement
        self.webAuthnPolicyPasswordlessCreateTimeout = web_authn_policy_passwordless_create_timeout
        self.webAuthnPolicyPasswordlessAvoidSameAuthenticatorRegister \
            = web_authn_policy_passwordless_avoid_same_authenticator_register
        self.webAuthnPolicyPasswordlessAcceptableAaguids = web_authn_policy_passwordless_acceptable_aaguids
        self.browserSecurityHeaders = browser_security_headers
        self.smtpServer = smtp_server
        self.loginTheme = login_theme
        self.accountTheme = account_theme
        self.adminTheme = admin_theme
        self.emailTheme = email_theme
        self.eventsEnabled = events_enabled
        self.eventsExpiration = events_expiration
        self.eventsListeners = events_listeners
        self.enabledEventTypes = enabled_event_types
        self.adminEventsEnabled = admin_events_enabled
        self.adminEventsDetailsEnabled = admin_events_details_enabled
        self.identityProviders = identity_providers
        self.identityProviderMappers = identity_provider_mappers
        self.internationalizationEnabled = internationalization_enabled
        self.supportedLocales = supported_locales
        self.browserFlow = browser_flow
        self.registrationFlow = registration_flow
        self.directGrantFlow = direct_grant_flow
        self.resetCredentialsFlow = reset_credentials_flow
        self.clientAuthenticationFlow = client_authentication_flow
        self.dockerAuthenticationFlow = docker_authentication_flow
        self.attributes = attributes
        self.userManagedAccessAllowed = user_managed_access_allowed
        self.clientProfiles = client_profiles
        self.clientPolicies = client_policies

    def __str__(self):
        return f"RealmRepresentation(" \
               f"id={self.id}" \
               f"realm={self.realm}" \
               f"displayName={self.displayName}" \
               f"notBefore={self.notBefore}" \
               f"revokeRefreshToken={self.revokeRefreshToken}" \
               f"refreshTokenMaxReuse={self.refreshTokenMaxReuse}" \
               f"accessTokenLifespan={self.accessTokenLifespan}" \
               f"accessTokenLifespanForImplicitFlow={self.accessTokenLifespanForImplicitFlow}" \
               f"ssoSessionIdleTimeout={self.ssoSessionIdleTimeout}" \
               f"ssoSessionMaxLifespan={self.ssoSessionMaxLifespan}" \
               f"ssoSessionIdleTimeoutRememberMe={self.ssoSessionIdleTimeoutRememberMe}" \
               f"ssoSessionMaxLifespanRememberMe={self.ssoSessionMaxLifespanRememberMe}" \
               f"offlineSessionIdleTimeout={self.offlineSessionIdleTimeout}" \
               f"offlineSessionMaxLifespanEnabled={self.offlineSessionMaxLifespanEnabled}" \
               f"offlineSessionMaxLifespan={self.offlineSessionMaxLifespan}" \
               f"clientSessionIdleTimeout={self.clientSessionIdleTimeout}" \
               f"clientSessionMaxLifespan={self.clientSessionMaxLifespan}" \
               f"clientOfflineSessionIdleTimeout={self.clientOfflineSessionIdleTimeout}" \
               f"clientOfflineSessionMaxLifespan={self.clientOfflineSessionMaxLifespan}" \
               f"accessCodeLifespan={self.accessCodeLifespan}" \
               f"accessCodeLifespanUserAction={self.accessCodeLifespanUserAction}" \
               f"accessCodeLifespanLogin={self.accessCodeLifespanLogin}" \
               f"actionTokenGeneratedByAdminLifespan={self.actionTokenGeneratedByAdminLifespan}" \
               f"actionTokenGeneratedByUserLifespan={self.actionTokenGeneratedByUserLifespan}" \
               f"oauth2DeviceCodeLifespan={self.oauth2DeviceCodeLifespan}" \
               f"oauth2DevicePollingInterval={self.oauth2DevicePollingInterval}" \
               f"enabled={self.enabled}" \
               f"sslRequired={self.sslRequired}" \
               f"registrationAllowed={self.registrationAllowed}" \
               f"registrationEmailAsUsername={self.registrationEmailAsUsername}" \
               f"rememberMe={self.rememberMe}" \
               f"verifyEmail={self.verifyEmail}" \
               f"loginWithEmailAllowed={self.loginWithEmailAllowed}" \
               f"duplicateEmailsAllowed={self.duplicateEmailsAllowed}" \
               f"resetPasswordAllowed={self.resetPasswordAllowed}" \
               f"editUsernameAllowed={self.editUsernameAllowed}" \
               f"bruteForceProtected={self.bruteForceProtected}" \
               f"permanentLockout={self.permanentLockout}" \
               f"maxFailureWaitSeconds={self.maxFailureWaitSeconds}" \
               f"minimumQuickLoginWaitSeconds={self.minimumQuickLoginWaitSeconds}" \
               f"waitIncrementSeconds={self.waitIncrementSeconds}" \
               f"quickLoginCheckMilliSeconds={self.quickLoginCheckMilliSeconds}" \
               f"maxDeltaTimeSeconds={self.maxDeltaTimeSeconds}" \
               f"failureFactor={self.failureFactor}" \
               f"defaultRole={self.defaultRole}" \
               f"requiredCredentials={self.requiredCredentials}" \
               f"passwordPolicy={self.passwordPolicy}" \
               f"otpPolicyType={self.otpPolicyType}" \
               f"otpPolicyAlgorithm={self.otpPolicyAlgorithm}" \
               f"otpPolicyInitialCounter={self.otpPolicyInitialCounter}" \
               f"otpPolicyDigits={self.otpPolicyDigits}" \
               f"otpPolicyLookAheadWindow={self.otpPolicyLookAheadWindow}" \
               f"otpPolicyPeriod={self.otpPolicyPeriod}" \
               f"otpSupportedApplications={self.otpSupportedApplications}" \
               f"webAuthnPolicyRpEntityName={self.webAuthnPolicyRpEntityName}" \
               f"webAuthnPolicySignatureAlgorithms={self.webAuthnPolicySignatureAlgorithms}" \
               f"webAuthnPolicyRpId={self.webAuthnPolicyRpId}" \
               f"webAuthnPolicyAttestationConveyancePreference={self.webAuthnPolicyAttestationConveyancePreference}" \
               f"webAuthnPolicyAuthenticatorAttachment={self.webAuthnPolicyAuthenticatorAttachment}" \
               f"webAuthnPolicyRequireResidentKey={self.webAuthnPolicyRequireResidentKey}" \
               f"webAuthnPolicyUserVerificationRequirement={self.webAuthnPolicyUserVerificationRequirement}" \
               f"webAuthnPolicyCreateTimeout={self.webAuthnPolicyCreateTimeout}" \
               f"webAuthnPolicyAvoidSameAuthenticatorRegister={self.webAuthnPolicyAvoidSameAuthenticatorRegister}" \
               f"webAuthnPolicyAcceptableAaguids={self.webAuthnPolicyAcceptableAaguids}" \
               f"webAuthnPolicyPasswordlessRpEntityName={self.webAuthnPolicyPasswordlessRpEntityName}" \
               f"webAuthnPolicyPasswordlessSignatureAlgorithms={self.webAuthnPolicyPasswordlessSignatureAlgorithms}" \
               f"webAuthnPolicyPasswordlessRpId={self.webAuthnPolicyPasswordlessRpId}" \
               f"webAuthnPolicyPasswordlessAttestationConveyancePreference=" \
               f"{self.webAuthnPolicyPasswordlessAttestationConveyancePreference}" \
               f"webAuthnPolicyPasswordlessAuthenticatorAttachment=" \
               f"{self.webAuthnPolicyPasswordlessAuthenticatorAttachment}" \
               f"webAuthnPolicyPasswordlessRequireResidentKey={self.webAuthnPolicyPasswordlessRequireResidentKey}" \
               f"webAuthnPolicyPasswordlessUserVerificationRequirement=" \
               f"{self.webAuthnPolicyPasswordlessUserVerificationRequirement}" \
               f"webAuthnPolicyPasswordlessCreateTimeout={self.webAuthnPolicyPasswordlessCreateTimeout}" \
               f"webAuthnPolicyPasswordlessAvoidSameAuthenticatorRegister=" \
               f"{self.webAuthnPolicyPasswordlessAvoidSameAuthenticatorRegister}" \
               f"webAuthnPolicyPasswordlessAcceptableAaguids={self.webAuthnPolicyPasswordlessAcceptableAaguids}" \
               f"browserSecurityHeaders={self.browserSecurityHeaders}" \
               f"smtpServer={self.smtpServer}" \
               f"loginTheme={self.loginTheme}" \
               f"accountTheme={self.accountTheme}" \
               f"adminTheme={self.adminTheme}" \
               f"emailTheme={self.emailTheme}" \
               f"eventsEnabled={self.eventsEnabled}" \
               f"eventsExpiration={self.eventsExpiration}" \
               f"eventsListeners={self.eventsListeners}" \
               f"enabledEventTypes={self.enabledEventTypes}" \
               f"adminEventsEnabled={self.adminEventsEnabled}" \
               f"adminEventsDetailsEnabled={self.adminEventsDetailsEnabled}" \
               f"identityProviders={self.identityProviders}" \
               f"identityProviderMappers={self.identityProviderMappers}" \
               f"internationalizationEnabled={self.internationalizationEnabled}" \
               f"supportedLocales={self.supportedLocales}" \
               f"browserFlow={self.browserFlow}" \
               f"registrationFlow={self.registrationFlow}" \
               f"directGrantFlow={self.directGrantFlow}" \
               f"resetCredentialsFlow={self.resetCredentialsFlow}" \
               f"clientAuthenticationFlow={self.clientAuthenticationFlow}" \
               f"dockerAuthenticationFlow={self.dockerAuthenticationFlow}" \
               f"attributes={self.attributes}" \
               f"userManagedAccessAllowed={self.userManagedAccessAllowed}" \
               f"clientProfiles={self.clientProfiles}" \
               f"clientPolicies={self.clientPolicies}" \
               f")"

    def get_post_data(self):
        return json.dumps({
            "id": self.id,
            "realm": self.realm,
            "displayName": self.displayName,
            "notBefore": self.notBefore,
            "revokeRefreshToken": self.revokeRefreshToken,
            "refreshTokenMaxReuse": self.refreshTokenMaxReuse,
            "accessTokenLifespan": self.accessTokenLifespan,
            "accessTokenLifespanForImplicitFlow": self.accessTokenLifespanForImplicitFlow,
            "ssoSessionIdleTimeout": self.ssoSessionIdleTimeout,
            "ssoSessionMaxLifespan": self.ssoSessionMaxLifespan,
            "ssoSessionIdleTimeoutRememberMe": self.ssoSessionIdleTimeoutRememberMe,
            "ssoSessionMaxLifespanRememberMe": self.ssoSessionMaxLifespanRememberMe,
            "offlineSessionIdleTimeout": self.offlineSessionIdleTimeout,
            "offlineSessionMaxLifespanEnabled": self.offlineSessionMaxLifespanEnabled,
            "offlineSessionMaxLifespan": self.offlineSessionMaxLifespan,
            "clientSessionIdleTimeout": self.clientSessionIdleTimeout,
            "clientSessionMaxLifespan": self.clientSessionMaxLifespan,
            "clientOfflineSessionIdleTimeout": self.clientOfflineSessionIdleTimeout,
            "clientOfflineSessionMaxLifespan": self.clientOfflineSessionMaxLifespan,
            "accessCodeLifespan": self.accessCodeLifespan,
            "accessCodeLifespanUserAction": self.accessCodeLifespanUserAction,
            "accessCodeLifespanLogin": self.accessCodeLifespanLogin,
            "actionTokenGeneratedByAdminLifespan": self.actionTokenGeneratedByAdminLifespan,
            "actionTokenGeneratedByUserLifespan": self.actionTokenGeneratedByUserLifespan,
            "oauth2DeviceCodeLifespan": self.oauth2DeviceCodeLifespan,
            "oauth2DevicePollingInterval": self.oauth2DevicePollingInterval,
            "enabled": self.enabled,
            "sslRequired": self.sslRequired,
            "registrationAllowed": self.registrationAllowed,
            "registrationEmailAsUsername": self.registrationEmailAsUsername,
            "rememberMe": self.rememberMe,
            "verifyEmail": self.verifyEmail,
            "loginWithEmailAllowed": self.loginWithEmailAllowed,
            "duplicateEmailsAllowed": self.duplicateEmailsAllowed,
            "resetPasswordAllowed": self.resetPasswordAllowed,
            "editUsernameAllowed": self.editUsernameAllowed,
            "bruteForceProtected": self.bruteForceProtected,
            "permanentLockout": self.permanentLockout,
            "maxFailureWaitSeconds": self.maxFailureWaitSeconds,
            "minimumQuickLoginWaitSeconds": self.minimumQuickLoginWaitSeconds,
            "waitIncrementSeconds": self.waitIncrementSeconds,
            "quickLoginCheckMilliSeconds": self.quickLoginCheckMilliSeconds,
            "maxDeltaTimeSeconds": self.maxDeltaTimeSeconds,
            "failureFactor": self.failureFactor,
            "defaultRole": self.defaultRole,
            "requiredCredentials": self.requiredCredentials,
            "passwordPolicy": self.passwordPolicy,
            "otpPolicyType": self.otpPolicyType,
            "otpPolicyAlgorithm": self.otpPolicyAlgorithm,
            "otpPolicyInitialCounter": self.otpPolicyInitialCounter,
            "otpPolicyDigits": self.otpPolicyDigits,
            "otpPolicyLookAheadWindow": self.otpPolicyLookAheadWindow,
            "otpPolicyPeriod": self.otpPolicyPeriod,
            "otpSupportedApplications": self.otpSupportedApplications,
            "webAuthnPolicyRpEntityName": self.webAuthnPolicyRpEntityName,
            "webAuthnPolicySignatureAlgorithms": self.webAuthnPolicySignatureAlgorithms,
            "webAuthnPolicyRpId": self.webAuthnPolicyRpId,
            "webAuthnPolicyAttestationConveyancePreference": self.webAuthnPolicyAttestationConveyancePreference,
            "webAuthnPolicyAuthenticatorAttachment": self.webAuthnPolicyAuthenticatorAttachment,
            "webAuthnPolicyRequireResidentKey": self.webAuthnPolicyRequireResidentKey,
            "webAuthnPolicyUserVerificationRequirement": self.webAuthnPolicyUserVerificationRequirement,
            "webAuthnPolicyCreateTimeout": self.webAuthnPolicyCreateTimeout,
            "webAuthnPolicyAvoidSameAuthenticatorRegister": self.webAuthnPolicyAvoidSameAuthenticatorRegister,
            "webAuthnPolicyAcceptableAaguids": self.webAuthnPolicyAcceptableAaguids,
            "webAuthnPolicyPasswordlessRpEntityName": self.webAuthnPolicyPasswordlessRpEntityName,
            "webAuthnPolicyPasswordlessSignatureAlgorithms": self.webAuthnPolicyPasswordlessSignatureAlgorithms,
            "webAuthnPolicyPasswordlessRpId": self.webAuthnPolicyPasswordlessRpId,
            "webAuthnPolicyPasswordlessAttestationConveyancePreference":
                self.webAuthnPolicyPasswordlessAttestationConveyancePreference,
            "webAuthnPolicyPasswordlessAuthenticatorAttachment": self.webAuthnPolicyPasswordlessAuthenticatorAttachment,
            "webAuthnPolicyPasswordlessRequireResidentKey": self.webAuthnPolicyPasswordlessRequireResidentKey,
            "webAuthnPolicyPasswordlessUserVerificationRequirement":
                self.webAuthnPolicyPasswordlessUserVerificationRequirement,
            "webAuthnPolicyPasswordlessCreateTimeout": self.webAuthnPolicyPasswordlessCreateTimeout,
            "webAuthnPolicyPasswordlessAvoidSameAuthenticatorRegister":
                self.webAuthnPolicyPasswordlessAvoidSameAuthenticatorRegister,
            "webAuthnPolicyPasswordlessAcceptableAaguids": self.webAuthnPolicyPasswordlessAcceptableAaguids,
            "browserSecurityHeaders": self.browserSecurityHeaders,
            "smtpServer": self.smtpServer,
            "loginTheme": self.loginTheme,
            "accountTheme": self.accountTheme,
            "adminTheme": self.adminTheme,
            "emailTheme": self.emailTheme,
            "eventsEnabled": self.eventsEnabled,
            "eventsExpiration": self.eventsExpiration,
            "eventsListeners": self.eventsListeners,
            "enabledEventTypes": self.enabledEventTypes,
            "adminEventsEnabled": self.adminEventsEnabled,
            "adminEventsDetailsEnabled": self.adminEventsDetailsEnabled,
            "identityProviders": self.identityProviders,
            "identityProviderMappers": self.identityProviderMappers,
            "internationalizationEnabled": self.internationalizationEnabled,
            "supportedLocales": self.supportedLocales,
            "browserFlow": self.browserFlow,
            "registrationFlow": self.registrationFlow,
            "directGrantFlow": self.directGrantFlow,
            "resetCredentialsFlow": self.resetCredentialsFlow,
            "clientAuthenticationFlow": self.clientAuthenticationFlow,
            "dockerAuthenticationFlow": self.dockerAuthenticationFlow,
            "attributes": self.attributes,
            "userManagedAccessAllowed": self.userManagedAccessAllowed,
            "clientProfiles": self.clientProfiles,
            "clientPolicies": self.clientPolicies,
        })


def construct_realm_representation(item):
    return RealmRepresentation(
        realm_id=item.get("id"),
        realm=item.get("realm"),
        display_name=item.get("displayName"),
        not_before=item.get("notBefore"),
        revoke_refresh_token=item.get("revokeRefreshToken"),
        refresh_token_max_reuse=item.get("refreshTokenMaxReuse"),
        access_token_lifespan=item.get("accessTokenLifespan"),
        access_token_lifespan_for_implicit_flow=item.get("accessTokenLifespanForImplicitFlow"),
        sso_session_idle_timeout=item.get("ssoSessionIdleTimeout"),
        sso_session_max_lifespan=item.get("ssoSessionMaxLifespan"),
        sso_session_idle_timeout_remember_me=item.get("ssoSessionIdleTimeoutRememberMe"),
        sso_session_max_lifespan_remember_me=item.get("ssoSessionMaxLifespanRememberMe"),
        offline_session_idle_timeout=item.get("offlineSessionIdleTimeout"),
        offline_session_max_lifespan_enabled=item.get("offlineSessionMaxLifespanEnabled"),
        offline_session_max_lifespan=item.get("offlineSessionMaxLifespan"),
        client_session_idle_timeout=item.get("clientSessionIdleTimeout"),
        client_session_max_lifespan=item.get("clientSessionMaxLifespan"),
        client_offline_session_idle_timeout=item.get("clientOfflineSessionIdleTimeout"),
        client_offline_session_max_lifespan=item.get("clientOfflineSessionMaxLifespan"),
        access_code_lifespan=item.get("accessCodeLifespan"),
        access_code_lifespan_user_action=item.get("accessCodeLifespanUserAction"),
        access_code_lifespan_login=item.get("accessCodeLifespanLogin"),
        action_token_generated_by_admin_lifespan=item.get("actionTokenGeneratedByAdminLifespan"),
        action_token_generated_by_user_lifespan=item.get("actionTokenGeneratedByUserLifespan"),
        oauth_2_device_code_lifespan=item.get("oauth2DeviceCodeLifespan"),
        oauth_2_device_polling_interval=item.get("oauth2DevicePollingInterval"),
        enabled=item.get("enabled"),
        ssl_required=item.get("sslRequired"),
        registration_allowed=item.get("registrationAllowed"),
        registration_email_as_username=item.get("registrationEmailAsUsername"),
        remember_me=item.get("rememberMe"),
        verify_email=item.get("verifyEmail"),
        login_with_email_allowed=item.get("loginWithEmailAllowed"),
        duplicate_emails_allowed=item.get("duplicateEmailsAllowed"),
        reset_password_allowed=item.get("resetPasswordAllowed"),
        edit_username_allowed=item.get("editUsernameAllowed"),
        brute_force_protected=item.get("bruteForceProtected"),
        permanent_lockout=item.get("permanentLockout"),
        max_failure_wait_seconds=item.get("maxFailureWaitSeconds"),
        minimum_quick_login_wait_seconds=item.get("minimumQuickLoginWaitSeconds"),
        wait_increment_seconds=item.get("waitIncrementSeconds"),
        quick_login_check_milli_seconds=item.get("quickLoginCheckMilliSeconds"),
        max_delta_time_seconds=item.get("maxDeltaTimeSeconds"),
        failure_factor=item.get("failureFactor"),
        default_role=item.get("defaultRole"),
        required_credentials=item.get("requiredCredentials"),
        password_policy=item.get("passwordPolicy"),
        otp_policy_type=item.get("otpPolicyType"),
        otp_policy_algorithm=item.get("otpPolicyAlgorithm"),
        otp_policy_initial_counter=item.get("otpPolicyInitialCounter"),
        otp_policy_digits=item.get("otpPolicyDigits"),
        otp_policy_look_ahead_window=item.get("otpPolicyLookAheadWindow"),
        otp_policy_period=item.get("otpPolicyPeriod"),
        otp_supported_applications=item.get("otpSupportedApplications"),
        web_authn_policy_rp_entity_name=item.get("webAuthnPolicyRpEntityName"),
        web_authn_policy_signature_algorithms=item.get("webAuthnPolicySignatureAlgorithms"),
        web_authn_policy_rp_id=item.get("webAuthnPolicyRpId"),
        web_authn_policy_attestation_conveyance_preference=item.get("webAuthnPolicyAttestationConveyancePreference"),
        web_authn_policy_authenticator_attachment=item.get("webAuthnPolicyAuthenticatorAttachment"),
        web_authn_policy_require_resident_key=item.get("webAuthnPolicyRequireResidentKey"),
        web_authn_policy_user_verification_requirement=item.get("webAuthnPolicyUserVerificationRequirement"),
        web_authn_policy_create_timeout=item.get("webAuthnPolicyCreateTimeout"),
        web_authn_policy_avoid_same_authenticator_register=item.get("webAuthnPolicyAvoidSameAuthenticatorRegister"),
        web_authn_policy_acceptable_aaguids=item.get("webAuthnPolicyAcceptableAaguids"),
        web_authn_policy_passwordless_rp_entity_name=item.get("webAuthnPolicyPasswordlessRpEntityName"),
        web_authn_policy_passwordless_signature_algorithms=item.get("webAuthnPolicyPasswordlessSignatureAlgorithms"),
        web_authn_policy_passwordless_rp_id=item.get("webAuthnPolicyPasswordlessRpId"),
        web_authn_policy_passwordless_attestation_conveyance_preference=item.get(
            "webAuthnPolicyPasswordlessAttestationConveyancePreference"),
        web_authn_policy_passwordless_authenticator_attachment=item.get(
            "webAuthnPolicyPasswordlessAuthenticatorAttachment"),
        web_authn_policy_passwordless_require_resident_key=item.get("webAuthnPolicyPasswordlessRequireResidentKey"),
        web_authn_policy_passwordless_user_verification_requirement=item.get(
            "webAuthnPolicyPasswordlessUserVerificationRequirement"),
        web_authn_policy_passwordless_create_timeout=item.get("webAuthnPolicyPasswordlessCreateTimeout"),
        web_authn_policy_passwordless_avoid_same_authenticator_register=item.get(
            "webAuthnPolicyPasswordlessAvoidSameAuthenticatorRegister"),
        web_authn_policy_passwordless_acceptable_aaguids=item.get("webAuthnPolicyPasswordlessAcceptableAaguids"),
        browser_security_headers=item.get("browserSecurityHeaders"),
        smtp_server=item.get("smtpServer"),
        login_theme=item.get("loginTheme"),
        account_theme=item.get("accountTheme"),
        admin_theme=item.get("adminTheme"),
        email_theme=item.get("emailTheme"),
        events_enabled=item.get("eventsEnabled"),
        events_expiration=item.get("eventsExpiration"),
        events_listeners=item.get("eventsListeners"),
        enabled_event_types=item.get("enabledEventTypes"),
        admin_events_enabled=item.get("adminEventsEnabled"),
        admin_events_details_enabled=item.get("adminEventsDetailsEnabled"),
        identity_providers=item.get("identityProviders"),
        identity_provider_mappers=item.get("identityProviderMappers"),
        internationalization_enabled=item.get("internationalizationEnabled"),
        supported_locales=item.get("supportedLocales"),
        browser_flow=item.get("browserFlow"),
        registration_flow=item.get("registrationFlow"),
        direct_grant_flow=item.get("directGrantFlow"),
        reset_credentials_flow=item.get("resetCredentialsFlow"),
        client_authentication_flow=item.get("clientAuthenticationFlow"),
        docker_authentication_flow=item.get("dockerAuthenticationFlow"),
        attributes=item.get("attributes"),
        user_managed_access_allowed=item.get("userManagedAccessAllowed"),
        client_profiles=item.get("clientProfiles"),
        client_policies=item.get("clientPolicies")
    )
