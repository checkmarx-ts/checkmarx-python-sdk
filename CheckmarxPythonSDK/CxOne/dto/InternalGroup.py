from dataclasses import dataclass


@dataclass
class InternalGroup:
    id: str = None
    name: str = None


def construct_internal_group(item):
    return InternalGroup(
        id=item.get("id"),
        name=item.get("name"),
    )
