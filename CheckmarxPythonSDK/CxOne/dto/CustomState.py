from dataclasses import dataclass


@dataclass
class CustomState:
    id: int = None
    name: str = None
    type: str = None
    is_allowed: str = None


def construct_custom_state(item):
    return CustomState(
        id=item.get("id"),
        name=item.get("name"),
        type=item.get("type"),
        is_allowed=item.get("isAllowed"),
    )
