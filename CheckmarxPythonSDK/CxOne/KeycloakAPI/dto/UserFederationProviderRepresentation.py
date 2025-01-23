class UserFederationProviderRepresentation:
    def __init__(self, changed_sync_period, config, display_name, full_sync_period,
                 user_federation_provider_representation_id, last_sync, priority, provider_name):
        self.changedSyncPeriod = changed_sync_period
        self.config = config
        self.displayName = display_name
        self.fullSyncPeriod = full_sync_period
        self.id = user_federation_provider_representation_id
        self.lastSync = last_sync
        self.priority = priority
        self.providerName = provider_name

    def __str__(self):
        return f"UserFederationProviderRepresentation(" \
               f"changedSyncPeriod={self.changedSyncPeriod}, " \
               f"config={self.config}, " \
               f"displayName={self.displayName}, " \
               f"fullSyncPeriod={self.fullSyncPeriod}, " \
               f"id={self.id}, " \
               f"lastSync={self.lastSync}, " \
               f"priority={self.priority}, " \
               f"providerName={self.providerName}" \
               f")"

    def to_dict(self):
        return {
            "changedSyncPeriod": self.changedSyncPeriod,
            "config": self.config,
            "displayName": self.displayName,
            "fullSyncPeriod": self.fullSyncPeriod,
            "id": self.id,
            "lastSync": self.lastSync,
            "priority": self.priority,
            "providerName": self.providerName,
        }


def construct_user_federation_provider_representation(item):
    return UserFederationProviderRepresentation(
        changed_sync_period=item.get("changedSyncPeriod"),
        config=item.get("config"),
        display_name=item.get("displayName"),
        full_sync_period=item.get("fullSyncPeriod"),
        user_federation_provider_representation_id=item.get("id"),
        last_sync=item.get("lastSync"),
        priority=item.get("priority"),
        provider_name=item.get("providerName"),
    )
