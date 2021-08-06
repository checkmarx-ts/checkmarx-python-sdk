class CxScanFileCountOfLanguage(object):

    def __init__(self, language, file_count):
        """

        Args:
            language (str):
            file_count (int):
        """
        self.language = language
        self.file_count = file_count

    def __str__(self):
        return """CxScanFileCountOfLanguage(language={}, file_count={})""".format(
            self.language, self.file_count
        )
