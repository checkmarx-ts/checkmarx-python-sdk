from dataclasses import dataclass
from typing import Optional

from .Line import Line


@dataclass
class Snippet:
    line: Optional[Line] = None
