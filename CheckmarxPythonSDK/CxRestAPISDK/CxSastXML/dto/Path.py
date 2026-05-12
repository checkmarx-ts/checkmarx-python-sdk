from dataclasses import dataclass
from typing import List, Optional

from .PathNode import PathNode


@dataclass
class Path:
    result_id: Optional[int] = None
    path_id: Optional[int] = None
    similarity_id: Optional[int] = None
    source_method: Optional[str] = None
    destination_method: Optional[str] = None
    path_nodes: Optional[List[PathNode]] = None

    @classmethod
    def from_dict(cls, item: dict, path_nodes=None) -> "Path":
        return cls(
            result_id=int(item.get("ResultId")),
            path_id=int(item.get("PathId")),
            similarity_id=int(item.get("SimilarityId")),
            source_method=item.get("SourceMethod"),
            destination_method=item.get("DestinationMethod"),
            path_nodes=path_nodes,
        )
