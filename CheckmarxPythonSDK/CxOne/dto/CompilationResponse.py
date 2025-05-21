from typing import List


class CompilationResponse(object):
    def __init__(self, failed_queries: List[dict] = None):
        self.failed_queries = failed_queries

    def __str__(self):
        return f"CompilationResponse(failed_queries={self.failed_queries})"
