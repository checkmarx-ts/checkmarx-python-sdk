from dataclasses import dataclass
from .Credentials import Credentials


@dataclass
class Git:
    """
    Git handler for scan
    Attributes:
        repoUrl (str): The URL of the Git repository to be scanned.
        branch (str): The Git branch of the project to be scanned.
        commit (str): he ID of the Git commit version to be scanned. Mutually exclusive to 'tag'.
        tag (str): The tag of the Git commit version to be scanned. Mutually exclusive to 'commit'.
        credentials (`Credentials`):
    """

    repoUrl: str
    branch: str
    commit: str = None
    tag: str = None
    credentials: Credentials = None
