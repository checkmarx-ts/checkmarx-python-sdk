from dataclasses import dataclass


@dataclass
class RealmEventsConfigRepresentation:
    admin_events_details_enabled: ... = None
    admin_events_enabled: ... = None
    enabled_event_types: ... = None
    events_enabled: ... = None
    events_expiration: ... = None
    events_listeners: ... = None

    @classmethod
    def from_dict(cls, item: dict) -> "RealmEventsConfigRepresentation":
        return cls(
            admin_events_details_enabled=item.get("adminEventsDetailsEnabled"),
            admin_events_enabled=item.get("adminEventsEnabled"),
            enabled_event_types=item.get("enabledEventTypes"),
            events_enabled=item.get("eventsEnabled"),
            events_expiration=item.get("eventsExpiration"),
            events_listeners=item.get("eventsListeners"),
        )
