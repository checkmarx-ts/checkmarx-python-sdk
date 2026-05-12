from dataclasses import dataclass


@dataclass
class Upload:
    """

    Args:
        uploadUrl (str): The URL pointing to the location of the uploaded file to scan.
                        Note: the URL was generated using POST /api/uploads.
        branch (str): The representative branch.
        repoUrl (str): The representative repository URL.
    """

    uploadUrl: str
    branch: str = None
    repoUrl: str = None
