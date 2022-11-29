class PlatformSummary(object):
    def __init__(self, platform, count):
        """

        Args:
            platform (str):
            count (int):
        """
        self.platform = platform
        self.count = count

    def __str__(self):
        return """PlatformSummary(platform={}, count={})""".format(
            self.platform, self.count
        )
