from dataclasses import dataclass


@dataclass
class Group:
    id: str = None
    name: str = None


def construct_group(item):
    return Group(
        id=item.get("id"),
        name=item.get("name")
    )
