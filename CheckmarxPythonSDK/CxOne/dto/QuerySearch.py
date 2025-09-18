from dataclasses import dataclass
from typing import List
from .Queries import Queries, construct_queries
from .QueryResult import QueryResult, construct_query_result


@dataclass
class QuerySearch:
    query: Queries = None
    results: List[QueryResult] = None


def construct_query_search(item):
    return QuerySearch(
        query=construct_queries(item.get("query")),
        results=[
            construct_query_result(query_result) for query_result in item.get("results", [])
        ]
    )
