from typing import List
from .Queries import Queries
from .QueryResult import QueryResult


class QuerySearch(object):
    def __init__(self, query: Queries = None, results: List[QueryResult] = None):
        self.query = query
        self.results = results

    def __str__(self):
        return f"QuerySearch(query={self.query}, results={self.results})"
