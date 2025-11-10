from dataclasses import dataclass
from typing import Dict, List, Any, Optional
from typing_extensions import Self
from inflection import camelize, underscore


@dataclass
class RealmEventsConfigRepresentation:
    events_enabled: Optional[bool] = None
    events_expiration: Optional[int] = None
    events_listeners: Optional[List[str]] = None
    enabled_event_types: Optional[List[str]] = None
    admin_events_enabled: Optional[bool] = None
    admin_events_details_enabled: Optional[bool] = None

    def to_dict(self) -> Dict[str, Any]:
        result: Dict[str, Any] = {}
        if self.events_enabled is not None:
            value = self.events_enabled
            result['eventsEnabled'] = value
        if self.events_expiration is not None:
            value = self.events_expiration
            result['eventsExpiration'] = value
        if self.events_listeners is not None:
            value = self.events_listeners
            result['eventsListeners'] = value
        if self.enabled_event_types is not None:
            value = self.enabled_event_types
            result['enabledEventTypes'] = value
        if self.admin_events_enabled is not None:
            value = self.admin_events_enabled
            result['adminEventsEnabled'] = value
        if self.admin_events_details_enabled is not None:
            value = self.admin_events_details_enabled
            result['adminEventsDetailsEnabled'] = value
        return result

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> Self:
        snake_data: Dict[str, Any] = {underscore(k): v for k, v in data.items()}

        required_fields = []
        missing = [f for f in required_fields if f not in snake_data]
        if missing:
            raise ValueError(f'missing required field: {missing}')
        return cls(**snake_data)
