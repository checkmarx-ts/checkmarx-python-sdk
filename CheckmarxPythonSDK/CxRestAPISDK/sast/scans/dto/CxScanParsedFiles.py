class CxScanParsedFiles(object):

    def __init__(self, scan_id, scanned_files_per_language):
        """

        Args:
            scan_id (str):
            scanned_files_per_language (`list` of `CxScanParsedFilesMetric`):
        """
        self.id = scan_id
        self.scanned_files_per_language = scanned_files_per_language

    def __str__(self):
        return """CxScanParsedFiles(id={}, scanned_files_per_language={})""".format(
            self.id, self.scanned_files_per_language
        )
