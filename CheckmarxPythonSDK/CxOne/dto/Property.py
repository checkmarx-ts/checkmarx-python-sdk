class Property(object):

    def __init__(self, key, value):
        """

        Args:
            key (str):
            value (value):
        """
        self.key = key
        self.value = value

    def __str__(self):
        return """Property(key={}, value={})""".format(
            self.key, self.value
        )
