from dataclasses import dataclass


@dataclass
class AuditEventLink:
    event_date: str = None
    url: str = None
    crc: str = None

    @classmethod
    def from_dict(cls, item: dict) -> "AuditEventLink":
        return cls(
            event_date=item.get("eventDate"),
            url=item.get("url"),
            crc=item.get("crc"),
        )
