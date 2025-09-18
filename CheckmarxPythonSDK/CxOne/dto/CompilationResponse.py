from typing import List
from dataclasses import dataclass


@dataclass
class CompilationResponse:
    failed_queries: List[dict] = None


def construct_compilation_response(item):
    return CompilationResponse(
        failed_queries=item.get("failedQueries")
    )
