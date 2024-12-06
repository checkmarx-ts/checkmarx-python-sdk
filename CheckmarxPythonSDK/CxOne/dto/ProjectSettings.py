from .Scanner import Scanner
from typing import List


class ProjectSettings(object):

    def __init__(self,
                 web_hook_enabled: bool,
                 decorate_pull_requests: bool,
                 scanners: List[Scanner],
                 tags: dict = None,
                 groups: List[str] = None,
                 is_private_package: bool = None,
                 ):
        """

        Args:
            web_hook_enabled (bool): If true, a webhook is enabled for each repo.
            decorate_pull_requests (bool): If true, pull request decorations will be sent to the repo.
                            Note: This requires webhookEnabled to be set as true.
            is_private_package (bool): If true the project will be marked as a private package for SCA scans. (Not
                currently supported)
            scanners (list of Scanner):
            tags (dict):
            groups (list of str):
        """
        self.webhookEnabled = web_hook_enabled
        self.decoratePullRequests = decorate_pull_requests
        self.isPrivatePackage = is_private_package
        self.scanners = scanners
        self.tags = tags
        self.groups = groups

    def __str__(self):
        return (f"ProjectSettings("
                f"webhookEnabled={self.webhookEnabled}, "
                f"decoratePullRequests={self.decoratePullRequests}, "
                f"isPrivatePackage={self.isPrivatePackage}, "
                f"scanners={self.scanners}, "
                f"tags={self.tags}, "
                f"groups={self.groups}"
                f")")

    def to_dict(self):
        result = {
            "decoratePullRequests": self.decoratePullRequests,
            "webhookEnabled": self.webhookEnabled,
            "scanners": [
                scanner.to_dict() for scanner in self.scanners
            ]
        }
        if self.tags is not None:
            result.update({"tags": self.tags})
        if self.groups is not None:
            result.update({"groups": self.groups})
        return result
