class TaskInfo(object):
    def __init__(self, source, timestamp, info):
        """

        Args:
            source (str): The service that generated the task event.
            timestamp (str): The time of the task event.
            info: An informative message describing the task event.
        """
        self.source = source
        self.timestamp = timestamp
        self.info = info

    def __str__(self):
        return """TaskInfo(source={}, timestamp={}, info={})""".format(
            self.source, self.timestamp, self.info
        )
