from dataclasses import dataclass


@dataclass
class RequestStatus:
    completed: bool = None
    status: str = None
    value: str = None


def construct_request_status(item):
    return RequestStatus(
        completed=item.get("completed"),
        status=item.get("status"),
        value=item.get("value")
    )
