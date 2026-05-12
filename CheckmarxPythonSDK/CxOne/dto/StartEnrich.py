from dataclasses import dataclass


@dataclass
class StartEnrich:
    """

    Args:
        uploadURL (str): URL obtained from the uploads service
    """

    uploadURL: str
