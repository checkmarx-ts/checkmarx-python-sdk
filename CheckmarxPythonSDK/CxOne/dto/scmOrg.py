class ScmOrg(object):
    def __init__(self, id, name, isUser):
        """

        Args:
            id (str): Severity enum of a result. Enum: [ HIGH, MEDIUM, LOW, INFO ]
            name (str):
            isUser (str):
        """
        self.id = id
        self.name = name
        self.isUser = isUser

    def __str__(self):
        return """scmOrg(id={}, name={})""".format(
            self.id, self.name
        )
