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

    def to_dict(self):
        return {
                "path": self.path,
                "name": self.name,
                "source": self.source,
            }
