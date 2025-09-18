from dataclasses import dataclass
from typing import List
from .WebHookEvent import WebHookEvent
from .WebHookConfig import WebHookConfig, construct_web_hook_config


@dataclass
class WebHookInput:
    """
    Attributes:
        name (str): A name for the webhook
        active (bool): Indicates whether a webhook is active or not
        enabled_events (List[WebHookEvent]): List of subscribed events. project_created only available for tenant level
        config: (WebHookConfig): Webhook configuration
    """
    name: str = None
    active: bool = None
    enabled_events: List[WebHookEvent] = None
    config: WebHookConfig = None

    def to_dict(self):
        return {
            "name": self.name,
            "active": self.active,
            "enabledEvents": self.enabled_events,
            "config": self.config.to_dict()
        }
