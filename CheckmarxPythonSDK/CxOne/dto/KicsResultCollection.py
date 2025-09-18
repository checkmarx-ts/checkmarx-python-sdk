from dataclasses import dataclass
from typing import List
from .KicsResult import KicsResult, construct_kics_result


@dataclass
class KicsResultCollection:
    results: List[KicsResult]
    total_count: int


def construct_kics_result_collection(item):
    return KicsResultCollection(
        results=[
            construct_kics_result(result) for result in item.get("results", [])
        ],
        total_count=item.get("totalCount"),
    )
