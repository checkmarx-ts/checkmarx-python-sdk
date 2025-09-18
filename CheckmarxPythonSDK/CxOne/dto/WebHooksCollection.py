from dataclasses import dataclass
from typing import List
from .WebHook import WebHook, construct_web_hook


@dataclass
class WebHooksCollection:
    total_count: int = None
    webhooks: List[WebHook] = None


def construct_web_hooks_collection(item):
    return WebHooksCollection(
        total_count=item.get("totalCount"),
        webhooks=[
            construct_web_hook(webhook) for webhook in item.get("webhooks")
        ]
    )
