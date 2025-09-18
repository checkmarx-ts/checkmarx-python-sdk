from dataclasses import dataclass
from typing import List


@dataclass
class RequestStatusDetectLanguages:
    completed: bool = None
    value: List[str] = None


def construct_request_status_detect_languages(item):
    return RequestStatusDetectLanguages(
        completed=item.get("completed"),
        value=item.get("value")
    )
