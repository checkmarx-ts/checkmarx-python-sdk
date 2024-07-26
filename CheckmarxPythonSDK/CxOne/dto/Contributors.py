class Contributors(object):

    def __init__(self, allowed_contributors, current_contributors):
        """

        Args:
            allowed_contributors (int):
            current_contributors (int):
        """
        self.allowed_contributors = allowed_contributors
        self.current_contributors = current_contributors

    def __str__(self):
        return """Contributors(allowed_contributors={}, current_contributors={})""".format(
            self.allowed_contributors, self.current_contributors
        )
