# encoding: utf-8


class CxScanState(object):
    """
    scan state
    """

    class LanguageState(object):
        """
        language state
        """
        def __init__(self, language_id, language_name, language_hash, state_creation_date):
            """

            :param language_id: int
            :param language_name: str
            :param language_hash: str
            :param state_creation_date: str
            """
            self.language_id = language_id
            self.language_name = language_name
            self.language_hash = language_hash
            self.state_creation_date = state_creation_date

    def __init__(self, path, source_id, files_count, lines_of_code, failed_lines_of_code, cx_version,
                 language_state_collection):
        """

        :param path:
        :param source_id:
        :param files_count:
        :param lines_of_code:
        :param failed_lines_of_code:
        :param cx_version:
        :param language_state_collection: list of CxScanState.LanguageState
        """
        self.path = path
        self.source_id = source_id
        self.files_count = files_count
        self.lines_of_code = lines_of_code
        self.failed_lines_of_code = failed_lines_of_code
        self.cx_version = cx_version
        self.language_state_collection = language_state_collection
