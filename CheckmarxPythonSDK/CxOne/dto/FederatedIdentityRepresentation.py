from dataclasses import dataclass


@dataclass
class FederatedIdentityRepresentation:
    identity_provider: str
    user_id: str
    user_name: str
