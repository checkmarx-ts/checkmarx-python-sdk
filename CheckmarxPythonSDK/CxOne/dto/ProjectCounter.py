class ProjectCounter(object):

    def __init__(self, value, count):
        """

        Args:
            value (str):
            count (int):
        """
        self.value = value
        self.count = count

    def __str__(self):
        return """ProjectCounter(value={}, count={})""".format(
            self.value, self.count
        )
