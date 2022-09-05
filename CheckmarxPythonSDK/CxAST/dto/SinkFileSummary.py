class SinkFileSummary(object):
    def __init__(self, sink_file, count):
        """

        Args:
            sink_file (str):
            count (int):
        """
        self.sinkFile = sink_file
        self.count = count

    def __str__(self):
        return """SinkFileSummary(sinkFile={}, count={})""".format(
            self.sinkFile, self.count
        )
