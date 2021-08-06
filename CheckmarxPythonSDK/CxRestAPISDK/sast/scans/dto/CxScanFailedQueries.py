class CxScanFailedQueries(object):

    def __init__(self, scan_id, failed_queries):
        """

        Args:
            scan_id (int):
            failed_queries (`list` of `str`):
        """
        self.id = scan_id
        self.failed_queries = failed_queries

    def __str__(self):
        return """CxScanFailedQueries(id={}, failed_queries={})""".format(
            self.id, self.failed_queries
        )
