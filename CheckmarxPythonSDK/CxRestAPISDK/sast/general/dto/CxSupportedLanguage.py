# encoding: utf-8

class CxSupportedLanguage(object):
    """
    The support status of a given programming language
    """
    def __init__(self, is_supported, language):
        self.is_supported = is_supported
        self.language = language

    def __str__(self):
        return """CxSupportedLanguage(is_supported={}, language={})""".format(
            self.is_supported, self.language
        )
