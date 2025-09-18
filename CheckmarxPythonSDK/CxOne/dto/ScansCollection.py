from dataclasses import dataclass
from typing import List
from .Scan import Scan, construct_scan


@dataclass
class ScansCollection:
    """

    Args:
        total_count (int): The total number of scans in your account.
        filtered_total_count (int): The number of scan results returned, based the applied filters.
        scans (`list` of `Scan`): An array containing the scan results returned, based on the applied filters.
    """
    total_count: int
    filtered_total_count: int
    scans: List[Scan]


def construct_scans_collection(item):
    return ScansCollection(
        total_count=item.get("totalCount"),
        filtered_total_count=item.get("filteredTotalCount"),
        scans=[
            construct_scan(scan) for scan in item.get("scans", [])
        ]
    )
