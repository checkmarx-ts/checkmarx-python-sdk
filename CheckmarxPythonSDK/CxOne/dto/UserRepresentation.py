class UserRepresentation:
    def __init__(self, access, attributes, client_consents, client_roles, created_timestamp, credentials,
                 disableable_credential_types, email, email_verified, enabled, federated_identities, federation_link,
                 first_name, groups, user_representation_id, last_name, not_before, origin, realm_roles,
                 required_actions, user_representation_self, service_account_client_id, username):
        self.access = access
        self.attributes = attributes
        self.clientConsents = client_consents
        self.clientRoles = client_roles
        self.createdTimestamp = created_timestamp
        self.credentials = credentials
        self.disableableCredentialTypes = disableable_credential_types
        self.email = email
        self.emailVerified = email_verified
        self.enabled = enabled
        self.federatedIdentities = federated_identities
        self.federationLink = federation_link
        self.firstName = first_name
        self.groups = groups
        self.id = user_representation_id
        self.lastName = last_name
        self.notBefore = not_before
        self.origin = origin
        self.realmRoles = realm_roles
        self.requiredActions = required_actions
        self.self = user_representation_self
        self.serviceAccountClientId = service_account_client_id
        self.username = username

    def __str__(self):
        return f"UserRepresentation(" \
               f"access={self.access}, " \
               f"attributes={self.attributes}, " \
               f"clientConsents={self.clientConsents}, " \
               f"clientRoles={self.clientRoles}, " \
               f"createdTimestamp={self.createdTimestamp}, " \
               f"credentials={self.credentials}, " \
               f"disableableCredentialTypes={self.disableableCredentialTypes}, " \
               f"email={self.email}, " \
               f"emailVerified={self.emailVerified}, " \
               f"enabled={self.enabled}, " \
               f"federatedIdentities={self.federatedIdentities}, " \
               f"federationLink={self.federationLink}, " \
               f"firstName={self.firstName}, " \
               f"groups={self.groups}, " \
               f"id={self.id}, " \
               f"lastName={self.lastName}, " \
               f"notBefore={self.notBefore}, " \
               f"origin={self.origin}, " \
               f"realmRoles={self.realmRoles}, " \
               f"requiredActions={self.requiredActions}, " \
               f"self={self.self}, " \
               f"serviceAccountClientId={self.serviceAccountClientId}, " \
               f"username={self.username}" \
               f")"

    def to_dict(self):
        return {
            "access": self.access,
            "attributes": self.attributes,
            "clientConsents": self.clientConsents,
            "clientRoles": self.clientRoles,
            "createdTimestamp": self.createdTimestamp,
            "credentials": self.credentials,
            "disableableCredentialTypes": self.disableableCredentialTypes,
            "email": self.email,
            "emailVerified": self.emailVerified,
            "enabled": self.enabled,
            "federatedIdentities": self.federatedIdentities,
            "federationLink": self.federationLink,
            "firstName": self.firstName,
            "groups": self.groups,
            "id": self.id,
            "lastName": self.lastName,
            "notBefore": self.notBefore,
            "origin": self.origin,
            "realmRoles": self.realmRoles,
            "requiredActions": self.requiredActions,
            "self": self.self,
            "serviceAccountClientId": self.serviceAccountClientId,
            "username": self.username,
        }


def construct_user_representation(item):
    return UserRepresentation(
        access=item.get("access"),
        attributes=item.get("attributes"),
        client_consents=item.get("clientConsents"),
        client_roles=item.get("clientRoles"),
        created_timestamp=item.get("createdTimestamp"),
        credentials=item.get("credentials"),
        disableable_credential_types=item.get("disableableCredentialTypes"),
        email=item.get("email"),
        email_verified=item.get("emailVerified"),
        enabled=item.get("enabled"),
        federated_identities=item.get("federatedIdentities"),
        federation_link=item.get("federationLink"),
        first_name=item.get("firstName"),
        groups=item.get("groups"),
        user_representation_id=item.get("id"),
        last_name=item.get("lastName"),
        not_before=item.get("notBefore"),
        origin=item.get("origin"),
        realm_roles=item.get("realmRoles"),
        required_actions=item.get("requiredActions"),
        user_representation_self=item.get("self"),
        service_account_client_id=item.get("serviceAccountClientId"),
        username=item.get("username"),
    )
