from dataclasses import dataclass
from .Metadata import Metadata


@dataclass
class QueryResponse:
    id: str = None
    name: str = None
    level: str = None
    path: str = None
    source: str = None
    metadata: Metadata = None

    @classmethod
    def from_dict(cls, item: dict) -> "QueryResponse":
        return cls(
            id=item.get("id"),
            name=item.get("name"),
            level=item.get("level"),
            path=item.get("path"),
            source=item.get("source"),
            metadata=Metadata.from_dict(item.get("metadata")),
        )
