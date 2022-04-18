from .Credentials import Credentials


class Git(object):
    """
    Git handler for scan
    """

    def __init__(self, branch, commit, tag, repo_url, credentials):
        """

        Args:
            branch (str): The Git branch of the project to be scanned.
            commit (str): he ID of the Git commit version to be scanned. Mutually exclusive to 'tag'.
            tag (str): The tag of the Git commit version to be scanned. Mutually exclusive to 'commit'.
            repo_url (str): The URL of the Git repository to be scanned.
            credentials (`Credentials`):
        """
        if not isinstance(credentials, Credentials):
            raise ValueError("credentials must be type: Credentials")

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
        return {
            "branch": self.branch,
            "commit": self.commit,
            "tag": self.tag,
            "repoUrl": self.repo_url,
            "credentials": self.credentials.as_dict(),
        }
