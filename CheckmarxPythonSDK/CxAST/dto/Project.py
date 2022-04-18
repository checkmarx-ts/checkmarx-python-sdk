class Project(object):

    def __init__(self, project_id, tags):
        """

        Args:
            project_id (str): A unique identifier for the project. For 'upload' projects, a value must be entered.
                For 'git' projects, this field can be empty and the repository URL will be designated as the project ID.
            tags (dict):
        """
        self.id = project_id
        self.tags = tags

    def __str__(self):
        return """Project(id={}, tags={})""".format(
            self.id, self.tags
        )

    def as_dict(self):
        return {
            "id": self.id,
            "tags": self.tags,
        }
