class RealmEventsConfigRepresentation:
    def __init__(self, admin_events_details_enabled, admin_events_enabled, enabled_event_types, events_enabled,
                 events_expiration, events_listeners):
        self.adminEventsDetailsEnabled = admin_events_details_enabled
        self.adminEventsEnabled = admin_events_enabled
        self.enabledEventTypes = enabled_event_types
        self.eventsEnabled = events_enabled
        self.eventsExpiration = events_expiration
        self.eventsListeners = events_listeners

    def __str__(self):
        return f"RealmEventsConfigRepresentation(" \
               f"adminEventsDetailsEnabled={self.adminEventsDetailsEnabled} " \
               f"adminEventsEnabled={self.adminEventsEnabled} " \
               f"enabledEventTypes={self.enabledEventTypes} " \
               f"eventsEnabled={self.eventsEnabled} " \
               f"eventsExpiration={self.eventsExpiration} " \
               f"eventsListeners={self.eventsListeners} " \
               f")"

    def to_dict(self):
        return {
            "adminEventsDetailsEnabled": self.adminEventsDetailsEnabled,
            "adminEventsEnabled": self.adminEventsEnabled,
            "enabledEventTypes": self.enabledEventTypes,
            "eventsEnabled": self.eventsEnabled,
            "eventsExpiration": self.eventsExpiration,
            "eventsListeners": self.eventsListeners,
        }


def construct_realm_events_config_representation(item):
    return RealmEventsConfigRepresentation(
        admin_events_details_enabled=item.get("adminEventsDetailsEnabled"),
        admin_events_enabled=item.get("adminEventsEnabled"),
        enabled_event_types=item.get("enabledEventTypes"),
        events_enabled=item.get("eventsEnabled"),
        events_expiration=item.get("eventsExpiration"),
        events_listeners=item.get("eventsListeners"),
    )
