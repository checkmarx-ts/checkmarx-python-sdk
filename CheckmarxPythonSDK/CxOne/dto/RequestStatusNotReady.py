from dataclasses import dataclass


@dataclass
class RequestStatusNotReady:
    completed: bool = None
    value: dict = None


def construct_request_status_not_ready(item):
    return RequestStatusNotReady(
        completed=item.get("completed"),
        value=item.get("value")
    )
