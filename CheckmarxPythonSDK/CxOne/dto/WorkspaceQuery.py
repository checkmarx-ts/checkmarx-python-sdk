from dataclasses import dataclass


@dataclass
class WorkspaceQuery:
    """

    Args:
        path (str):
        name (str):
        source (str):
    """

    path: str
    name: str
    source: str
