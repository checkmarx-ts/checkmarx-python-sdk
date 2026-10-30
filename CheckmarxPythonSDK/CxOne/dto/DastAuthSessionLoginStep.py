from dataclasses import dataclass, field
from typing import List, Optional


@dataclass
class DastAuthSessionLoginStep:
    """An entry in `loginSteps[]` on GET /authSession/{envId}/reportData.

    `web_elements` and `messages` are left as raw dicts/lists — their
    schemas (WebElementItem/MessageItem) weren't populated in any
    observed response, so the exact wire shape isn't confirmed.
    """
    description: Optional[str] = None
    url: Optional[str] = None
    screenshot: Optional[str] = None
    web_elements: List[dict] = field(default_factory=list)
    messages: List[dict] = field(default_factory=list)

    @classmethod
    def from_dict(cls, item: dict) -> "DastAuthSessionLoginStep":
        return cls(
            description=item.get("description"),
            url=item.get("url"),
            screenshot=item.get("screenshot"),
            web_elements=list(item.get("webElements") or []),
            messages=list(item.get("messages") or []),
        )
