from dataclasses import dataclass


@dataclass
class ImportRequest:
    """

    Args:
        projectId (str): The id of the project for which the results are being imported
        uploadUrl (str): The url to upload the file
    """

    projectId: str
    uploadUrl: str
