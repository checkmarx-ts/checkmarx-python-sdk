from typing import List
from dataclasses import dataclass


@dataclass
class CompilationResponse:
    failed_queries: List[dict] = None
