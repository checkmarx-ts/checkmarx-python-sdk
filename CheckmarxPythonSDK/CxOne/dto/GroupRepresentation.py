from dataclasses import dataclass


@dataclass
class GroupRepresentation:
    id: str = None
    name: str = None
    path: str = None


def construct_group_representation(item):
    return GroupRepresentation(
        id=item.get("id"),
        name=item.get("name"),
        path=item.get("path"),
    )
