#encoding: utf-8

from .CxScanResult import CxScanResult

class CxScanResultsPage:

    def __init__(self, scan_id, offset, limit, total_count, results):
        """
        Args:
            scan_id (int): the unique id of the scan
            offset (int): the page offset
            limit (int): the page size
            total_count (int): the total number of results
            results (`list` of `CxResult`)
        """
        self.scan_id = scan_id
        self.offset = offset
        self.limit = limit
        self.total_count = total_count
        self.results = results

    @staticmethod
    def from_dict(d):
        """
        Args:
            d (dict): a dict containing the scan results page data
        """
        results = [CxScanResult.from_dict(d2) for d2 in d['results']]
        return CxScanResultsPage(scan_id=d['scanId'],
                                   offset=d['offset'],
                                   limit=d['limit'],
                                   total_count=d['totalCount'],
                                   results = results)

    def __str__(self):
        return """CxScanResultsPage(scan_id={}, offset={}, limit={},
               total_count={}, results={})""".format(self.scan_id,
                                                     self.offset,
                                                     self.limit,
                                                     self.total_count,
                                                     self.results)
