class SubCheck(object):
    def __init__(self, name, success, errors):
        """

        Args:
            name (str):
            success (bool):
            errors (list of str):
        """
        self.name = name
        self.success = success
        self.errors = errors

    def __str__(self):
        return """SubCheck(name={}, success={}, errors={})""".format(
            self.name, self.success, self.errors
        )
