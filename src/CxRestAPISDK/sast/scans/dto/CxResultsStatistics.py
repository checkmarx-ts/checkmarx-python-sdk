# encoding: utf-8


class CxResultsStatistics(object):
    """
    scan results statistics
    """

    def __init__(self, link):
        """

        Args:
            link (str):
        """
        self.link = link

    def __str__(self):
        return "CxResultsStatistics(link={})".format(
            self.link
        )
