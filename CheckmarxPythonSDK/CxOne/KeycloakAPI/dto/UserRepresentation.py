from dataclasses import dataclass
from typing import Dict, List, Any, Optional
from typing_extensions import Self
from inflection import camelize, underscore
from .CredentialRepresentation import CredentialRepresentation
from .FederatedIdentityRepresentation import FederatedIdentityRepresentation
from .SocialLinkRepresentation import SocialLinkRepresentation
from .UserConsentRepresentation import UserConsentRepresentation
from .UserProfileMetadata import UserProfileMetadata


@dataclass
class UserRepresentation:
    username: str
    email: str
    first_name: str
    last_name: str
    self: Optional[str] = None
    id: Optional[str] = None
    origin: Optional[str] = None
    created_timestamp: Optional[int] = None
    enabled: Optional[bool] = None
    totp: Optional[bool] = None
    email_verified: Optional[bool] = None
    federation_link: Optional[str] = None
    service_account_client_id: Optional[str] = None
    attributes: Optional[Dict[str, Any]] = None
    credentials: Optional[List[CredentialRepresentation]] = None
    disableable_credential_types: Optional[List[str]] = None
    required_actions: Optional[List[str]] = None
    federated_identities: Optional[List[FederatedIdentityRepresentation]] = None
    realm_roles: Optional[List[str]] = None
    client_roles: Optional[Dict[str, Any]] = None
    client_consents: Optional[List[UserConsentRepresentation]] = None
    not_before: Optional[int] = None
    application_roles: Optional[Dict[str, Any]] = None
    social_links: Optional[List[SocialLinkRepresentation]] = None
    groups: Optional[List[str]] = None
    access: Optional[Dict[str, Any]] = None
    user_profile_metadata: Optional[UserProfileMetadata] = None

    def to_dict(self) -> Dict[str, Any]:
        result: Dict[str, Any] = {}
        if self.self is not None:
            value = self.self
            result['self'] = value
        if self.id is not None:
            value = self.id
            result['id'] = value
        if self.origin is not None:
            value = self.origin
            result['origin'] = value
        if self.created_timestamp is not None:
            value = self.created_timestamp
            result['createdTimestamp'] = value
        if self.username is not None:
            value = self.username
            result['username'] = value
        if self.enabled is not None:
            value = self.enabled
            result['enabled'] = value
        if self.totp is not None:
            value = self.totp
            result['totp'] = value
        if self.email_verified is not None:
            value = self.email_verified
            result['emailVerified'] = value
        if self.first_name is not None:
            value = self.first_name
            result['firstName'] = value
        if self.last_name is not None:
            value = self.last_name
            result['lastName'] = value
        if self.email is not None:
            value = self.email
            result['email'] = value
        if self.federation_link is not None:
            value = self.federation_link
            result['federationLink'] = value
        if self.service_account_client_id is not None:
            value = self.service_account_client_id
            result['serviceAccountClientId'] = value
        if self.attributes is not None:
            value = self.attributes
            result['attributes'] = value
        if self.credentials is not None:
            value = [item.to_dict() for item in self.credentials]
            result['credentials'] = value
        if self.disableable_credential_types is not None:
            value = self.disableable_credential_types
            result['disableableCredentialTypes'] = value
        if self.required_actions is not None:
            value = self.required_actions
            result['requiredActions'] = value
        if self.federated_identities is not None:
            value = [item.to_dict() for item in self.federated_identities]
            result['federatedIdentities'] = value
        if self.realm_roles is not None:
            value = self.realm_roles
            result['realmRoles'] = value
        if self.client_roles is not None:
            value = self.client_roles
            result['clientRoles'] = value
        if self.client_consents is not None:
            value = [item.to_dict() for item in self.client_consents]
            result['clientConsents'] = value
        if self.not_before is not None:
            value = self.not_before
            result['notBefore'] = value
        if self.application_roles is not None:
            value = self.application_roles
            result['applicationRoles'] = value
        if self.social_links is not None:
            value = [item.to_dict() for item in self.social_links]
            result['socialLinks'] = value
        if self.groups is not None:
            value = self.groups
            result['groups'] = value
        if self.access is not None:
            value = self.access
            result['access'] = value
        if self.user_profile_metadata is not None:
            value = self.user_profile_metadata.to_dict()
            result['userProfileMetadata'] = value
        return result

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> Self:
        snake_data: Dict[str, Any] = {underscore(k): v for k, v in data.items()}

        if 'user_profile_metadata' in snake_data and snake_data['user_profile_metadata'] is not None:
            snake_data['user_profile_metadata'] = UserProfileMetadata.from_dict(snake_data['user_profile_metadata'])
        if 'credentials' in snake_data and snake_data['credentials'] is not None:
            snake_data['credentials'] = [
                CredentialRepresentation.from_dict(item) for item in snake_data['credentials']
            ]
        if 'federated_identities' in snake_data and snake_data['federated_identities'] is not None:
            snake_data['federated_identities'] = [
                FederatedIdentityRepresentation.from_dict(item) for item in snake_data['federated_identities']
            ]
        if 'client_consents' in snake_data and snake_data['client_consents'] is not None:
            snake_data['client_consents'] = [
                UserConsentRepresentation.from_dict(item) for item in snake_data['client_consents']
            ]
        if 'social_links' in snake_data and snake_data['social_links'] is not None:
            snake_data['social_links'] = [
                SocialLinkRepresentation.from_dict(item) for item in snake_data['social_links']
            ]
        required_fields = []
        missing = [f for f in required_fields if f not in snake_data]
        if missing:
            raise ValueError(f'missing required field: {missing}')
        return cls(**snake_data)
