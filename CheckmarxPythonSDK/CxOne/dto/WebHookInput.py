from dataclasses import dataclass
from typing import List
from .WebHookEvent import WebHookEvent
from .WebHookConfig import WebHookConfig


@dataclass
class WebHookInput:
    """
    Attributes:
        name (str): A name for the webhook
        active (bool): Indicates whether a webhook is active or not
        enabledEvents (List[WebHookEvent]): List of subscribed events. project_created only available for tenant level
        config: (WebHookConfig): Webhook configuration
    """

    name: str = None
    active: bool = None
    enabledEvents: List[WebHookEvent] = None
    config: WebHookConfig = None
