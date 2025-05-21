from typing import List
from .Session import Session


class Sessions(object):
    def __init__(self, available: bool = None, metadata: List[Session] = None):
        self.available = available
        self.metadata = metadata

    def __str__(self):
        return f"Sessions(available={self.available}, metadata={self.metadata})"
