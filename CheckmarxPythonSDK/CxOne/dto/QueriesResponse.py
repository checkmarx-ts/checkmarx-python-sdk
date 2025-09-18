from dataclasses import dataclass


@dataclass
class QueriesResponse:
    """

    Args:
        name (str):
        is_active (bool):
        last_modified (str):
    """
    name: str = None
    is_active: bool = None
    last_modified: str = None


def construct_queries_response(item):
    return QueriesResponse(
        name=item.get("name"),
        is_active=item.get("isActive"),
        last_modified=item.get("lastModified")
    )
