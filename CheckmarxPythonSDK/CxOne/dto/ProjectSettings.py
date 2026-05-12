from dataclasses import dataclass
from .Scanner import Scanner
from typing import List


@dataclass
class ProjectSettings:
    """

    Args:
        webhookEnabled (bool): If true, a webhook is enabled for each repo.
        decoratePullRequests (bool): If true, pull request decorations will be sent to the repo.
                        Note: This requires webhookEnabled to be set as true.
        isPrivatePackage (bool): If true the project will be marked as a private package for SCA scans. (Not
            currently supported)
        scanners (list of Scanner):
        tags (dict):
        groups (list of str):
    """

    webhookEnabled: bool = None
    decoratePullRequests: bool = None
    isPrivatePackage: bool = None
    scanners: List[Scanner] = None
    tags: dict = None
    groups: List[str] = None
