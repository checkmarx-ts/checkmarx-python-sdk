class CxScanSucceededGeneralQueries(object):

    def __init__(self, scan_id, general_queries_result_count):
        """

        Args:
            scan_id (int):
            general_queries_result_count (dict):

        """
        self.scan_id = scan_id
        self.general_queries_result_count = general_queries_result_count

    def __str__(self):
        return """CxScanSucceededGeneralQueries(scan_id={}, general_queries_result_count={})""".format(
            self.scan_id, self.general_queries_result_count
        )
