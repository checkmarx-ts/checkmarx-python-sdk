from dataclasses import dataclass


@dataclass
class Queries:
    id: int = None
    name: str = None
    group: str = None
    level: str = None
    path: str = None
    lang: str = None
    modify: str = None
    is_executable: bool = None

    @classmethod
    def from_dict(cls, item: dict) -> "Queries":
        return cls(
            id=item.get("id"),
            name=item.get("name"),
            group=item.get("group"),
            level=item.get("level"),
            path=item.get("path"),
            lang=item.get("lang"),
            modify=item.get("modify"),
            is_executable=item.get("isExecutable"),
        )
