from dataclasses import dataclass
from typing import List
from .DebugMessage import DebugMessage


@dataclass
class DebugMessageResponse:
    data: List[DebugMessage] = None
    total_count: int = None


def construct_debug_message_response(item):
    return DebugMessageResponse(
        data=item.get("data"),
        total_count=item.get("totalCount")
    )
