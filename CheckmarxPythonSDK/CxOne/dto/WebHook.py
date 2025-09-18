from dataclasses import dataclass
from typing import List
from .WebHookEvent import WebHookEvent
from .WebHookConfig import WebHookConfig, construct_web_hook_config


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


def construct_web_hook(item):
    return WebHook(
        id=item.get("id"),
        name=item.get("name"),
        active=item.get("active"),
        enabled_events=[
            WebHookEvent(event) for event in item.get("enabledEvents")
        ],
        config=construct_web_hook_config(item.get("config")),
        created_at=item.get("createdAt"),
        updated_at=item.get("updatedAt")
    )
