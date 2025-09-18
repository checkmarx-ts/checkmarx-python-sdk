from dataclasses import dataclass


@dataclass
class Queries:
    id: int = None
    name: str = None
    group: str = None
    level: str = None
    lang: str = None
    modify: str = None
    is_executable: bool = None


def construct_queries(item):
    return Queries(
        id=item.get("id"),
        name=item.get("name"),
        group=item.get("group"),
        level=item.get("level"),
        lang=item.get("lang"),
        modify=item.get("modify"),
        is_executable=item.get("isExecutable")
    )
