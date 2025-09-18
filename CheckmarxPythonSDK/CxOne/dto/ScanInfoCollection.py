from dataclasses import dataclass
from .ScanInfo import ScanInfo, construct_scan_info
from typing import List


@dataclass
class ScanInfoCollection:
    """

    Args:
        total_count (int): The number of records matching the applied filter.
        scans (list of ScanInfo): Scans of that specific group.
        missing (list str): List of scan ids that wasn't found.
    """
    total_count: int
    scans: List[ScanInfo]
    missing: List[str]


def construct_scan_info_collection(item):
    return ScanInfoCollection(
        total_count=item.get("totalCount"),
        scans=[
            construct_scan_info(scan_info) for scan_info in item.get("scans", [])
        ],
        missing=item.get("missing")
    )
