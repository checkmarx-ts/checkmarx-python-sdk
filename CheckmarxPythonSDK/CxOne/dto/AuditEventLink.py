from dataclasses import dataclass


@dataclass
class AuditEventLink:
    event_date: str = None
    url: str = None
    crc: str = None


def construct_audit_event_link(item):
    return AuditEventLink(
        event_date=item.get("eventDate"),
        url=item.get("url"),
        crc=item.get("crc"),
    )
