from dataclasses import dataclass


@dataclass
class RequestStatus:
    completed: bool = None
    status: str = None
    value: str = None

    @classmethod
    def from_dict(cls, item: dict) -> "RequestStatus":
        return cls(
            completed=item.get("completed"),
            status=item.get("status"),
            value=item.get("value"),
        )
