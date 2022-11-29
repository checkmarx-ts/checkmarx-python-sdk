# encoding: utf-8
from .Credentials import Credentials
from ..utilities import type_check


class Git(object):
    """
    Git handler for scan
    """

    def __init__(self, repo_url, branch, commit=None, tag=None, credentials=None):
        """

        Args:
            repo_url (str): The URL of the Git repository to be scanned.
            branch (str): The Git branch of the project to be scanned.
            commit (str): he ID of the Git commit version to be scanned. Mutually exclusive to 'tag'.
            tag (str): The tag of the Git commit version to be scanned. Mutually exclusive to 'commit'.
            credentials (`Credentials`):
        """
        type_check(repo_url, str)
        type_check(branch, str)
        type_check(commit, str)
        type_check(tag, str)
        type_check(credentials, Credentials)

        self.branch = branch
        self.commit = commit
        self.tag = tag
        self.repo_url = repo_url
        self.credentials = credentials

    def __str__(self):
        return """Git(branch={}, commit={}, tag={}, repo_url={}, credentials={})""".format(
            self.branch, self.commit, self.tag, self.repo_url, self.credentials
        )

    def as_dict(self):
        data = {
            "repoUrl": self.repo_url,
            "branch": self.branch,
            "commit": self.commit,
            "tag": self.tag,
        }
        if self.credentials:
            data.update({"credentials": self.credentials.as_dict()})
        else:
            data.update({"credentials": self.credentials})
        return data
