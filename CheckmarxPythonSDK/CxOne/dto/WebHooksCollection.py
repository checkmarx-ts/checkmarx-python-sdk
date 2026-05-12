from dataclasses import dataclass, field
from typing import List
from .WebHook import WebHook


@dataclass
class WebHooksCollection:
    total_count: int = None
    webhooks: List[WebHook] = field(default_factory=list)

    @classmethod
    def from_dict(cls, item: dict) -> "WebHooksCollection":
        return cls(
            total_count=item.get("totalCount"),
            webhooks=[WebHook.from_dict(w) for w in (item.get("webhooks") or [])],
        )
