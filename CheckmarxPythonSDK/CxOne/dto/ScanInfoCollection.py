class ScanInfoCollection(object):

    def __init__(self, total_count, scans, missing):
        """

        Args:
            total_count (int): The number of records matching the applied filter.
            scans (list of ScanInfo): Scans of that specific group.
            missing (list str): List of scan ids that wasn't found.
        """
        self.total_count = total_count
        self.scans = scans
        self.missing = missing

    def __str__(self):
        return """ScanInfoCollection(total_count={}, scans={}, missing={})""".format(
            self.total_count, self.scans, self.missing
        )
