from dataclasses import dataclass
from typing import List
from .TimeStamp import TimeStamp


@dataclass
class ExecutionResponse:
    scan_id: str = None
    time_stamp: TimeStamp = None
    queries: List[dict] = None
