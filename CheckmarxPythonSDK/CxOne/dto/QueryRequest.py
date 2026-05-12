from dataclasses import dataclass
from .Metadata import Metadata


@dataclass
class QueryRequest:
    path: str = None
    name: str = None
    source: str = None
    metadata: Metadata = None
