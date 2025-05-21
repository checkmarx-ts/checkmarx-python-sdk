from typing import List
from .ResultResponse import ResultResponse


class ResultsResponse(object):
    def __init__(self, data: List[ResultResponse] = None, total_count: int = None):
        self.data = data
        self.totalCount = total_count

    def __str__(self):
        return f"ResultsResponse(data={self.data}, totalCount={self.totalCount})"
