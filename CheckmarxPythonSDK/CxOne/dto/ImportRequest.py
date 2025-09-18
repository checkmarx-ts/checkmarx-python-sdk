from dataclasses import dataclass


@dataclass
class ImportRequest:
    """

    Args:
        project_id (str): The id of the project for which the results are being imported
        upload_url (str): The url to upload the file
    """
    project_id: str
    upload_url: str

    def to_dict(self):
        return {
                "projectId": self.project_id,
                "uploadUrl": self.upload_url,
            }


def construct_import_request(item):
    return ImportRequest(
        project_id=item.get("projectId"),
        upload_url=item.get("uploadUrl")
    )
