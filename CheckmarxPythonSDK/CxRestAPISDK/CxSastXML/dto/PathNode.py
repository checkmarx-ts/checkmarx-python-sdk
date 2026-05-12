from dataclasses import dataclass
from typing import Optional

from .Snippet import Snippet


@dataclass
class PathNode:
    file_name: Optional[str] = None
    line_number: Optional[int] = None
    column_number: Optional[int] = None
    node_id: Optional[int] = None
    node_name: Optional[str] = None
    node_type: Optional[str] = None
    node_name_length: Optional[int] = None
    snippet: Optional[Snippet] = None
