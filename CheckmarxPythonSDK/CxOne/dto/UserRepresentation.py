from dataclasses import dataclass
from typing import List
from .CredentialRepresentation import CredentialRepresentation
from .FederatedIdentityRepresentation import FederatedIdentityRepresentation
from .SocialLinkRepresentation import SocialLinkRepresentation
from .UserConsentRepresentation import UserConsentRepresentation
from .UserProfileMetadata import UserProfileMetadata


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
