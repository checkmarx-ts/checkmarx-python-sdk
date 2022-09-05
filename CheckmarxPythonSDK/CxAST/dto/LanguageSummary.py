class LanguageSummary(object):
    def __init__(self, language, count):
        """

        Args:
            language (str):
            count (int):
        """
        self.language = language
        self.count = count

    def __str__(self):
        return """LanguageSummary(language={}, count={})""".format(
            self.language, self.count
        )
