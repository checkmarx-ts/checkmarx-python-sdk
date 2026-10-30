from dataclasses import dataclass
from typing import Optional


@dataclass
class CloudConnectionStatus:
    """Status of a cloud connection for a specific consumer. An entry in
    CloudConnectionItem.statuses."""
    status: Optional[str] = None
    status_message: Optional[str] = None
    consumer_name: Optional[str] = None

    @classmethod
    def from_dict(cls, item: dict) -> "CloudConnectionStatus":
        return cls(
            status=item.get("status"),
            status_message=item.get("statusMessage"),
            consumer_name=item.get("consumerName"),
        )
