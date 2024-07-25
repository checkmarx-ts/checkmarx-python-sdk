import json


class StartEnrich(object):

    def __init__(self, upload_url):
        """

        Args:
            upload_url (str): URL obtained from the uploads service
        """
        self.upload_url = upload_url

    def __str__(self):
        return """StartEnrich(upload_url={})""".format(
            self.upload_url
        )

    def get_post_data(self):
        return json.dumps(
            {
                "uploadURL": self.upload_url,
            }
        )
