class ScansCollection(object):
    def __init__(self, total_count, filtered_total_count, scans):
        """

        Args:
            total_count (int): The total number of scans in your account.
            filtered_total_count (int): The number of scan results returned, based the applied filters.
            scans (`list` of `Scan`): An array containing the scan results returned, based on the applied filters.
        """
        self.totalCount = total_count
        self.filteredTotalCount = filtered_total_count
        self.scans = scans

    def __str__(self):
        return """ScansCollection(totalCount={}, filteredTotalCount={}, scans={})""".format(
            self.totalCount, self.filteredTotalCount, self.scans
        )
