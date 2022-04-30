import json
class WorkspaceQuery(object):
    def __init__(self, path, name, source):
        """

        Args:
            path (str):
            name (str):
            source (str):
        """
        self.path = path
        self.name = name
        self.source = source

    def __str__(self):
        return """WorkspaceQuery(path={}, name={}, source={})""".format(
            self.path, self.name, self.source
        )

    def get_post_data(self):
        return json.dumps(
            {
                "path": self.path,
                "name": self.name,
                "source": self.source,
            }
        )
