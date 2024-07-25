import json


class CreateEnrichAccount(object):

    def __init__(self, name, external_id):
        """

        Args:
            name (str): The account name
            external_id (str): A unique identifier provided by Checkmarx
        """
        self.name = name
        self.external_id = external_id

    def __str__(self):
        return """CreateEnrichAccount(name={}, external_id={})""".format(
            self.name, self.external_id
        )

    def get_post_data(self):
        return json.dumps(
            {
                "name": self.name,
                "externalID": self.external_id
            }
        )
