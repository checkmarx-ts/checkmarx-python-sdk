from dataclasses import dataclass


@dataclass
class QueryResult:
    content: str = None
    line_number: int = None


def construct_query_result(item):
    return QueryResult(
        content=item.get("content"),
        line_number=item.get("lineNumber")
    )
