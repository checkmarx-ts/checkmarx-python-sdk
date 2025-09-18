from dataclasses import dataclass


@dataclass
class Upload:
    """

    Args:
        upload_url (str): The URL pointing to the location of the uploaded file to scan.
                        Note: the URL was generated using POST /api/uploads.
        branch (str): The representative branch.
        repo_url (str): The representative repository URL.
    """
    upload_url: str
    branch: str = None
    repo_url: str = None

    def to_dict(self):
        data = {"uploadUrl": self.upload_url}
        if self.branch:
            data.update({"branch": self.branch})
        if self.repo_url:
            data.update({"repoUrl": self.repo_url})
        return data
