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

    def to_dict(self):
        return {
            "id": self.id,
            "displayName": self.display_name,
            "providerName": self.provider_name,
            "config": self.config,
            "priority": self.priority,
            "fullSyncPeriod": self.full_sync_period,
            "changedSyncPeriod": self.changed_sync_period,
            "lastSync": self.last_sync,
        }


def construct_user_federation_provider_representation(item):
    return UserFederationProviderRepresentation(
        id=item.get("id"),
        display_name=item.get("displayName"),
        provider_name=item.get("providerName"),
        config=item.get("config"),
        priority=item.get("priority"),
        full_sync_period=item.get("fullSyncPeriod"),
        changed_sync_period=item.get("changedSyncPeriod"),
        last_sync=item.get("lastSync"),
    )
