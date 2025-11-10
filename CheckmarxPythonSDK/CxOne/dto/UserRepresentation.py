from dataclasses import dataclass
from typing import List
from .CredentialRepresentation import CredentialRepresentation, construct_credential_representation
from .FederatedIdentityRepresentation import (FederatedIdentityRepresentation,
                                              construct_federated_identity_representation)
from .SocialLinkRepresentation import SocialLinkRepresentation, construct_social_link_representation
from .UserConsentRepresentation import UserConsentRepresentation, construct_user_consent_representation
from .UserProfileMetadata import UserProfileMetadata, construct_user_profile_metadata


@dataclass
class UserRepresentation:
    username: str
    first_name: str
    last_name: str
    email: str
    self: str = None
    id: str = None
    origin: str = None
    created_timestamp: int = None
    enabled: bool = None
    totp: bool = None
    email_verified: bool = None
    federation_link: str = None
    service_account_client_id: str = None
    attributes: dict = None
    credentials: List[CredentialRepresentation] = None
    disable_able_credential_types: List[str] = None
    required_actions: List[str] = None
    federated_identities: List[FederatedIdentityRepresentation] = None
    realm_roles: List[str] = None
    client_roles: dict = None
    client_consents: List[UserConsentRepresentation] = None
    not_before: int = None
    application_roles: dict = None
    social_links: List[SocialLinkRepresentation] = None
    groups: List[str] = None
    access: bool = None
    user_profile_metadata: UserProfileMetadata = None

    def to_dict(self):
        return {
            "self": self.self,
            "id": self.id,
            "origin": self.origin,
            "createdTimestamp": self.created_timestamp,
            "username": self.username,
            "enabled": self.enabled,
            "totp": self.totp,
            "emailVerified": self.email_verified,
            "firstName": self.first_name,
            "lastName": self.last_name,
            "email": self.email,
            "federationLink": self.federation_link,
            "serviceAccountClientId": self.service_account_client_id,
            "attributes": self.attributes,
            "credentials": [credential.to_dict() for credential in self.credentials],
            "disableableCredentialTypes": self.disable_able_credential_types,
            "requiredActions": self.required_actions,
            "federatedIdentities": [identity.to_dict() for identity in self.federated_identities],
            "realmRoles": self.realm_roles,
            "clientRoles": self.client_roles,
            "clientConsents": [client_consent.to_dict() for client_consent in self.client_consents],
            "notBefore": self.not_before,
            "applicationRoles": self.application_roles,
            "socialLinks": [social_link.to_dict() for social_link in self.social_links],
            "groups": self.groups,
            "access": self.access,
            "userProfileMetadata": self.user_profile_metadata.to_dict()
        }


def construct_user_representation(item):
    return UserRepresentation(
        self=item.get("self"),
        id=item.get("id"),
        origin=item.get("origin"),
        created_timestamp=item.get("createdTimestamp"),
        username=item.get("username"),
        enabled=item.get("enabled"),
        totp=item.get("totp"),
        email_verified=item.get("emailVerified"),
        first_name=item.get("firstName"),
        last_name=item.get("lastName"),
        email=item.get("email"),
        federation_link=item.get("federationLink"),
        service_account_client_id=item.get("serviceAccountClientId"),
        attributes=item.get("attributes"),
        credentials=[construct_credential_representation(credential) for credential in item.get("credentials")],
        disable_able_credential_types=item.get("disableableCredentialTypes"),
        required_actions=item.get("requiredActions"),
        federated_identities=[
            construct_federated_identity_representation(identity) for identity in item.get("federatedIdentities")
        ],
        realm_roles=item.get("realmRoles"),
        client_roles=item.get("clientRoles"),
        client_consents=[construct_user_consent_representation(consent) for consent in item.get("clientConsents")],
        not_before=item.get("notBefore"),
        application_roles=item.get("applicationRoles"),
        social_links=[construct_social_link_representation(social_link) for social_link in item.get("socialLinks")],
        groups=item.get("groups"),
        access=item.get("access"),
        user_profile_metadata=construct_user_profile_metadata(item.get("userProfileMetadata")),
    )
