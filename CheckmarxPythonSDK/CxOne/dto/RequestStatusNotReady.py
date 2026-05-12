from dataclasses import dataclass


@dataclass
class RequestStatusNotReady:
    completed: bool = None
    value: dict = None
