class QueriesResponse(object):
    def __init__(self, name, is_active, last_modified):
        """

        Args:
            name (str):
            is_active (bool):
            last_modified (str):
        """
        self.name = name
        self.isActive = is_active
        self.lastModified = last_modified

    def __str__(self):
        return """QueriesResponse(name={}, isActive={}, lastModified={})""".format(
            self.name, self.isActive, self.lastModified
        )
