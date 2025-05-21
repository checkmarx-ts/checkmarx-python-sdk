from typing import List
from .TimeStamp import TimeStamp


class ExecutionResponse(object):
    def __init__(self, scan_id: str = None, time_stamp: TimeStamp = None, queries: List[dict] = None):
        self.scanId = scan_id
        self.timeStamp = time_stamp
        self.queries = queries

    def __str__(self):
        return f"ExecutionResponse(scanId={self.scanId}, timeStamp={self.timeStamp}, queries={self.queries})"
