class SourceFileSummary(object):
    def __init__(self, source_file, count):
        """

        Args:
            source_file (str):
            count (int):
        """
        self.sourceFile = source_file
        self.count = count

    def __str__(self):
        return """SourceFileSummary(sourceFile={}, count={})""".format(
            self.sourceFile, self.count
        )
