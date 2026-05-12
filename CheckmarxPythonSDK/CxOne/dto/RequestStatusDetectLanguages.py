from dataclasses import dataclass
from typing import List


@dataclass
class RequestStatusDetectLanguages:
    completed: bool = None
    value: List[str] = None
