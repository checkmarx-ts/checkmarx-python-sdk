from dataclasses import dataclass
from typing import List
from .ResultResponse import ResultResponse, construct_result_response


@dataclass
class ResultsResponse:
    data: List[ResultResponse] = None
    total_count: int = None


def construct_results_response(item):
    return ResultsResponse(
        data=[
            construct_result_response(result) for result in item.get("data", [])
        ],
        total_count=item.get("totalCount")
    )
