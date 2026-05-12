from dataclasses import dataclass
from typing import List
from .FileInfo import FileInfo


@dataclass
class Tree:
    full_path: str = None
    name: str = None
    is_dir: bool = None
    files: List[FileInfo] = None

    @classmethod
    def from_dict(cls, item: dict) -> "Tree":
        return cls(
            full_path=item.get("FullPath"),
            name=item.get("name"),
            is_dir=item.get("IsDir"),
            files=[FileInfo.from_dict(f) for f in (item.get("Files") or [])],
        )
