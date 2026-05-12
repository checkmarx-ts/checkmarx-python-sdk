from dataclasses import dataclass
from typing import List, Optional


@dataclass
class FirstAdminUserRequest:
    username: Optional[str] = None
    password: Optional[str] = None
    firstName: Optional[str] = None
    lastName: Optional[str] = None
    email: Optional[str] = None


@dataclass
class LDAPRoleMappingRequest:
    roleId: Optional[int] = None
    ldapGroupDn: Optional[str] = None
    ldapGroupDisplayName: Optional[str] = None


@dataclass
class LDAPTeamMappingRequest:
    teamId: Optional[int] = None
    ldapGroupDn: Optional[str] = None
    ldapGroupDisplayName: Optional[str] = None


@dataclass
class LDAPServerRequest:
    password: Optional[str] = None
    active: Optional[bool] = None
    name: Optional[str] = None
    host: Optional[str] = None
    port: Optional[int] = None
    username: Optional[str] = None
    useSsl: Optional[bool] = None
    verifySslCertificate: Optional[bool] = None
    baseDn: Optional[str] = None
    additionalUserDn: Optional[str] = None
    userObjectFilter: Optional[str] = None
    userObjectClass: Optional[str] = None
    usernameAttribute: Optional[str] = None
    firstNameAttribute: Optional[str] = None
    lastNameAttribute: Optional[str] = None
    emailAttribute: Optional[str] = None
    ldapDirectoryType: Optional[str] = None
    ssoEnabled: Optional[bool] = None
    synchronizationEnabled: Optional[bool] = None
    defaultTeamId: Optional[int] = None
    defaultRoleId: Optional[int] = None
    updateTeamAndRoleUponLoginEnabled: Optional[bool] = None
    periodicalSynchronizationEnabled: Optional[bool] = None
    advancedTeamAndRoleMappingEnabled: Optional[bool] = None
    additionalGroupDn: Optional[str] = None
    groupObjectClass: Optional[str] = None
    groupObjectFilter: Optional[str] = None
    groupNameAttribute: Optional[str] = None
    groupMembersAttribute: Optional[str] = None
    userMembershipAttribute: Optional[str] = None


@dataclass
class MyProfileUpdateRequest:
    firstName: Optional[str] = None
    lastName: Optional[str] = None
    email: Optional[str] = None
    phoneNumber: Optional[str] = None
    cellPhoneNumber: Optional[str] = None
    jobTitle: Optional[str] = None
    other: Optional[str] = None
    country: Optional[str] = None
    localeId: Optional[int] = None


@dataclass
class OIDCClientRequest:
    updateAccessTokenClaimsOnRefresh: Optional[bool] = None
    accessTokenType: Optional[int] = None
    includeJwtId: Optional[bool] = None
    alwaysIncludeUserClaimsInIdToken: Optional[bool] = None
    clientId: Optional[str] = None
    clientName: Optional[str] = None
    allowOfflineAccess: Optional[bool] = None
    clientSecrets: Optional[List[str]] = None
    allowedGrantTypes: Optional[List[str]] = None
    allowedScopes: Optional[List[str]] = None
    enabled: Optional[bool] = None
    requireClientSecret: Optional[bool] = None
    redirectUris: Optional[List[str]] = None
    postLogoutRedirectUris: Optional[List[str]] = None
    frontChannelLogoutUri: Optional[str] = None
    frontChannelLogoutSessionRequired: Optional[bool] = None
    backChannelLogoutUri: Optional[str] = None
    backChannelLogoutSessionRequired: Optional[bool] = None
    identityTokenLifetime: Optional[int] = None
    accessTokenLifetime: Optional[int] = None
    authorizationCodeLifetime: Optional[int] = None
    absoluteRefreshTokenLifetime: Optional[int] = None
    slidingRefreshTokenLifetime: Optional[int] = None
    refreshTokenUsage: Optional[int] = None
    refreshTokenExpiration: Optional[int] = None
    allowedCorsOrigins: Optional[List[str]] = None
    allowAccessTokensViaBrowser: Optional[bool] = None
    claims: Optional[List[str]] = None
    clientClaimsPrefix: Optional[str] = None


@dataclass
class RoleRequest:
    name: Optional[str] = None
    description: Optional[str] = None
    permissionIds: Optional[List[int]] = None


@dataclass
class SMTPSettingRequest:
    password: Optional[str] = None
    host: Optional[str] = None
    port: Optional[int] = None
    encryptionType: Optional[str] = None
    fromAddress: Optional[str] = None
    useDefaultCredentials: Optional[str] = None
    username: Optional[str] = None
    recieverEmail: Optional[str] = None


@dataclass
class UserRequest:
    username: Optional[str] = None
    password: Optional[str] = None
    roleIds: Optional[List[int]] = None
    teamIds: Optional[List[int]] = None
    authenticationProviderId: Optional[int] = None
    firstName: Optional[str] = None
    lastName: Optional[str] = None
    email: Optional[str] = None
    phoneNumber: Optional[str] = None
    cellPhoneNumber: Optional[str] = None
    jobTitle: Optional[str] = None
    other: Optional[str] = None
    country: Optional[str] = None
    active: Optional[str] = None
    expirationDate: Optional[str] = None
    allowedIpList: Optional[str] = None
    localeId: Optional[int] = None
    creationDate: Optional[str] = None
