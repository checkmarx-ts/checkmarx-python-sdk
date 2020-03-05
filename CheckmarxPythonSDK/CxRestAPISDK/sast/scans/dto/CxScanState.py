# encoding: utf-8


class CxScanState(object):
    """
    scan state, used in CxScanDetail
    """

    def __init__(self, path, source_id, files_count, lines_of_code, failed_lines_of_code, cx_version,
                 language_state_collection):
        """

        Args:
            path (str):
            source_id (str):
            files_count (int):
            lines_of_code (int):
            failed_lines_of_code (int):
            cx_version (str):
            language_state_collection (:obj:`list` of :obj:`CxLanguageSate`):
        """
        self.path = path
        self.source_id = source_id
        self.files_count = files_count
        self.lines_of_code = lines_of_code
        self.failed_lines_of_code = failed_lines_of_code
        self.cx_version = cx_version
        self.language_state_collection = language_state_collection

    def __str__(self):
        return """CxScanState(path={}, source_id={}, files_count={}, lines_of_code={}, failed_lines_of_code={},
                cx_version={}, language_state_collection={})""".format(
            self.path, self.source_id, self.files_count, self.lines_of_code, self.failed_lines_of_code,
            self.cx_version, self.language_state_collection
        )
