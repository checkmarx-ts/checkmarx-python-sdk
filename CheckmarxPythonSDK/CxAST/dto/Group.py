class Group(object):
    def __init__(self, group_id, name):
        """

        Args:
            id (str):
            name (str):
        """
        self.id = group_id
        self.name = name

    def __str__(self):
        return """Group(id={}, name={})""".format(
            self.id, self.name
        )
