from dataclasses import dataclass
from typing import List
from .WebHookEvent import WebHookEvent
from .WebHookConfig import WebHookConfig


@dataclass
class WebHook:
    """

    Attributes:
        id (str): A unique identifier for an webhook
        name (str): A name for the webhook
        active (bool): Indicates whether a webhook is active or not
        enabled_events (List[WebHookEvent]): List of subscribed events
        config (WebHookConfig): Webhook configuration
        created_at (str):
        updated_at (str):
    """

    id: str = None
    name: str = None
    active: bool = None
    enabled_events: List[WebHookEvent] = None
    config: WebHookConfig = None
    created_at: str = None
    updated_at: str = None

    @classmethod
    def from_dict(cls, item: dict) -> "WebHook":
        return cls(
            id=item.get("id"),
            name=item.get("name"),
            active=item.get("active"),
            enabled_events=[WebHookEvent(e) for e in (item.get("enabledEvents") or [])],
            config=WebHookConfig.from_dict(item.get("config")),
            created_at=item.get("createdAt"),
            updated_at=item.get("updatedAt"),
        )
