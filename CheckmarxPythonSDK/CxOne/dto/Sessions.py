from dataclasses import dataclass
from typing import List
from .Session import Session, construct_session


@dataclass
class Sessions:
    available: bool = None
    metadata: List[Session] = None


def construct_sessions(item):
    return Sessions(
        available=item.get("available"),
        metadata=[
            construct_session(session) for session in item.get("metadata", [])
        ]
    )
