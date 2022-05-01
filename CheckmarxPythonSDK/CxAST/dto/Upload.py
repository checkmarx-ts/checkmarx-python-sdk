# encoding: utf-8
from ..utilities import type_check


class Upload(object):
    """
    Upload handler for scan
    """
    def __init__(self, upload_url, branch=None, repo_url=None):
        """

        Args:
            upload_url (str): The URL pointing to the location of the uploaded file to scan.
                            Note: the URL was generated using POST /api/uploads.
            branch (str): The representative branch.
            repo_url (str): The representive repository URL.
        """
        type_check(upload_url, str)
        type_check(branch, str)
        type_check(repo_url, str)

        self.branch = branch
        self.repo_url = repo_url
        self.upload_url = upload_url

    def __str__(self):
        return """Upload(branch={}, repo_url={}, upload_url={})""".format(
            self.branch, self.repo_url, self.upload_url
        )

    def as_dict(self):
        data = {"uploadUrl": self.upload_url}
        if self.branch:
            data.update({"branch": self.branch})
        if self.repo_url:
            data.update({"repoUrl": self.repo_url})
        return data
