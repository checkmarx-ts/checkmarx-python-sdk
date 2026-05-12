from dataclasses import dataclass
from typing import List
from .Queries import Queries
from .QueryResult import QueryResult


@dataclass
class QuerySearch:
    query: Queries = None
    results: List[QueryResult] = None

    @classmethod
    def from_dict(cls, item: dict) -> "QuerySearch":
        return cls(
            query=Queries.from_dict(item.get("query")),
            results=[QueryResult.from_dict(r) for r in (item.get("results") or [])],
        )
