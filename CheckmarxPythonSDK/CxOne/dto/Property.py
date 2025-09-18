from dataclasses import dataclass


@dataclass
class Property:
    """

    Args:
        key (str):
        value (str):
    """
    key: str = None
    value: str = None


def construct_property(item):
    return Property(
        key=item.get("key"),
        value=item.get("value")
    )
