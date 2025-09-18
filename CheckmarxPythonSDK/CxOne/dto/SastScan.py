from dataclasses import dataclass
from .Property import Property, construct_property
from typing import List


@dataclass
class SastScan:
    """

    Attributes:
        scan_id (str):
        state (str):
        queue_at (str):
        allocated_at (str):
        running_at (str):
        engine (str):
        properties (list of Property):
    """
    scan_id: str
    state: str
    queue_at: str
    allocated_at: str
    running_at: str
    engine: str
    properties: List[Property]


def construct_sast_scan(item):
    return SastScan(
        scan_id=item.get("scanId"),
        state=item.get("state"),
        queue_at=item.get("queueAt"),
        allocated_at=item.get("allocatedAt"),
        running_at=item.get("runningAt"),
        engine=item.get("engine"),
        properties=[
            construct_property(scan_property) for scan_property in item.get("properties", [])
        ]
    )
