class QueryDescriptionSampleCode(object):
    def __init__(self, programming_language, code, title):
        """

        Args:
            programming_language (str):
            code (str):
            title (str):
        """
        self.progLanguage = programming_language
        self.code = code
        self.title = title

    def __str__(self):
        return """QueryDescriptionSampleCode(progLanguage={}, code={}, title={})""".format(
            self.progLanguage, self.code, self.title
        )
