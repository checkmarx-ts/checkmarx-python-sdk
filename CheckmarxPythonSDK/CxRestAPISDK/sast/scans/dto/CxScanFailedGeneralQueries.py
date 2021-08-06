class CxScanFailedGeneralQueries(object):

    def __init__(self, scan_id, failed_general_queries):
        """

        Args:
            scan_id (int):
            failed_general_queries (`list` of str):
        """
        self.scan_id = scan_id
        self.failed_general_queries = failed_general_queries

    def __str__(self):
        return """CxScanFailedGeneralQueries(id={}, failed_general_queries={})""".format(
            self.scan_id, self.failed_general_queries
        )