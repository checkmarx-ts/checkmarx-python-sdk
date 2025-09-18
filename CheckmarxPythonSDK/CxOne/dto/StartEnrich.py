from dataclasses import dataclass


@dataclass
class StartEnrich:
    """

    Args:
        upload_url (str): URL obtained from the uploads service
    """
    upload_url: str

    def to_dict(self):
        return {
                "uploadURL": self.upload_url,
            }
