# encoding: utf-8
class Upload(object):
    """
    Upload handler for scan
    """
    def __init__(self, branch, repo_url, upload_url):
        """

        Args:
            branch (str): The representative branch.
            repo_url (str): The representive repository URL.
            upload_url (str): The URL pointing to the location of the uploaded file to scan.
                            Note: the URL was generated using POST /api/uploads.
        """
        self.branch = branch
        self.repo_url = repo_url
        self.upload_url = upload_url

    def __str__(self):
        return """Upload(branch={}, repo_url={}, upload_url={})""".format(
            self.branch, self.repo_url, self.upload_url
        )

    def as_dict(self):
        return {
            "branch": self.branch,
            "repoUrl": self.repo_url,
            "uploadUrl": self.upload_url,
        }
