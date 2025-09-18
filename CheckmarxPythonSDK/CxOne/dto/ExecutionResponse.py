from dataclasses import dataclass
from typing import List
from .TimeStamp import TimeStamp


@dataclass
class ExecutionResponse:
    scan_id: str = None
    time_stamp: TimeStamp = None
    queries: List[dict] = None


def construct_execution_response(item):
    return ExecutionResponse(
        scan_id=item.get("scanId"),
        time_stamp=item.get("timeStamp"),
        queries=item.get("queries")
    )
