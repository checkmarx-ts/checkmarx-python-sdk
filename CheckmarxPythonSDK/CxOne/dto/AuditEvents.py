from .AuditEventLink import AuditEventLink, construct_audit_event_link
from .AuditEvent import AuditEvent, construct_audit_event
from dataclasses import dataclass
from typing import List


@dataclass
class AuditEvents:
    links: List[AuditEventLink] = None
    events: List[AuditEvent] = None


def construct_audit_events(item):
    return AuditEvents(
        links=[
            construct_audit_event_link(link) for link in item.get("links", [])
        ],
        events=[
            construct_audit_event(event) for event in item.get("events", [])
        ],
    )
