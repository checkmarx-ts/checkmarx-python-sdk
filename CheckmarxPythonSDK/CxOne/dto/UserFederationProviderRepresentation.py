from dataclasses import dataclass


@dataclass
class UserFederationProviderRepresentation:
    id: str
    display_name: str
    provider_name: str
    config: dict
    priority: int
    full_sync_period: int
    changed_sync_period: int
    last_sync: int
