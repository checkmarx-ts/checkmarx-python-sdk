from typing import List
from .DebugMessage import DebugMessage


class DebugMessageResponse(object):
    def __init__(self, data: List[DebugMessage] = None, total_count: int = None):
        self.data = data
        self.totalCount = total_count

    def __str__(self):
        return f"DebugMessageResponse(data={self.data}, totalCount={self.totalCount})"
