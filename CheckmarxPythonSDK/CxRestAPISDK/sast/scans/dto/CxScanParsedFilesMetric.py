class CxScanParsedFilesMetric(object):
    def __init__(self, language, parsed_successfully, parsed_unsuccessfully, parsed_partially):
        """

        Args:
            language (str):
            parsed_successfully (str):
            parsed_unsuccessfully (str):
            parsed_partially (str):
        """
        self.language = language
        self.parsed_successfully = parsed_successfully
        self.parsed_unsuccessfully = parsed_unsuccessfully
        self.parsed_partially = parsed_partially

    def __str__(self):
        return """CxScanParsedFilesMetric(language={}, parsed_successfully={}, parsed_unsuccessfully={}, 
                parsed_partially={}) """.format(
            self.language, self.parsed_successfully, self.parsed_unsuccessfully, self.parsed_partially
        )
