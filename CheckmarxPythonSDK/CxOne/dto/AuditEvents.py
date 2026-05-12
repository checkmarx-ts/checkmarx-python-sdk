from .AuditEventLink import AuditEventLink
from .AuditEvent import AuditEvent
from dataclasses import dataclass
from typing import List


@dataclass
class AuditEvents:
    links: List[AuditEventLink] = None
    events: List[AuditEvent] = None

    @classmethod
    def from_dict(cls, item: dict) -> "AuditEvents":
        return cls(
            links=[
                AuditEventLink.from_dict(link) for link in (item.get("links") or [])
            ],
            events=[
                AuditEvent.from_dict(event) for event in (item.get("events") or [])
            ],
        )
