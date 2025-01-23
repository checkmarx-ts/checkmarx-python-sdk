
class ImportRequest(object):

    def __init__(self, project_id, upload_url):
        """

        Args:
            project_id (str): The id of the project for which the results are being imported
            upload_url (str): The url to upload the file
        """
        self.project_id = project_id
        self.upload_url = upload_url

    def __str__(self):
        return """ImportRequest(project_id={}, upload_url={})""".format(
            self.project_id, self.upload_url
        )

    def to_dict(self):
        return {
                "projectId": self.project_id,
                "uploadUrl": self.upload_url,
            }
