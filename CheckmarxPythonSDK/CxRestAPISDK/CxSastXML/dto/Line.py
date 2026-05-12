from dataclasses import dataclass
from typing import Optional


@dataclass
class Line:
    number: Optional[int] = None
    code: Optional[str] = None
