
class ResultsODataAPI(object):

    def __init__(self):
        self.retry = 0

    def get_results_for_a_specific_scan_id(self, scan_id):
        """
        http://localhost.checkmarx.net/Cxwebinterface/odata/v1/Scans(1006992)/Results?$top=10&$skip=0
        http://localhost.checkmarx.net/Cxwebinterface/odata/v1/Scans(1006992)/Results?$top=10&$skip=10

        Args:
            scan_id (int):

        Returns:

        """
        pass

    def retrieve_the_query_that_was_run_for_a_particular_unique_scan_result(self):
        """
        Requested result: selects a particular unique scan result and lists the query (SQL Injection, etc.) that was run

        Query used for retrieving the data:
        http://localhost/Cxwebinterface/odata/v1/Results(Id=18,ScanId=1000001)?$expand=Query($select=Name)

        Returns:

        """
