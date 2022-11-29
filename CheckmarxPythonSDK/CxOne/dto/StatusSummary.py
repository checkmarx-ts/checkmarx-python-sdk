class StatusSummary(object):
    def __init__(self, status, count):
        """

        Args:
            status (str): Status enum of a result Enum: [ NEW, RECURRENT ]
            count (int):
        """
        self.status = status
        self.count = count

    def __str__(self):
        return """StatusSummary(status={}, count={})""".format(
            self.status, self.count
        )
