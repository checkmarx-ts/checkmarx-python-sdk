from dataclasses import dataclass
from .Credentials import Credentials
from ..utilities import type_check


@dataclass
class Git:
    """
    Git handler for scan
    Attributes:
        repo_url (str): The URL of the Git repository to be scanned.
        branch (str): The Git branch of the project to be scanned.
        commit (str): he ID of the Git commit version to be scanned. Mutually exclusive to 'tag'.
        tag (str): The tag of the Git commit version to be scanned. Mutually exclusive to 'commit'.
        credentials (`Credentials`):
    """
    repo_url: str
    branch: str
    commit: str = None
    tag: str = None
    credentials: Credentials = None

    def to_dict(self):
        data = {
            "repoUrl": self.repo_url,
            "branch": self.branch,
            "commit": self.commit,
            "tag": self.tag,
        }
        if self.credentials:
            data.update({"credentials": self.credentials.to_dict()})
        else:
            data.update({"credentials": self.credentials})
        return data
