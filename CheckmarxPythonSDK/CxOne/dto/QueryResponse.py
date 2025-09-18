from dataclasses import dataclass
from .Metadata import Metadata, construct_metadata


@dataclass
class QueryResponse:
    id: str = None
    name: str = None
    level: str = None
    path: str = None
    source: str = None
    metadata: Metadata = None


def construct_query_response(item):
    return QueryResponse(
        id=item.get("id"),
        name=item.get("name"),
        level=item.get("level"),
        path=item.get("path"),
        source=item.get("source"),
        metadata=construct_metadata(item.get("metadata"))
    )
