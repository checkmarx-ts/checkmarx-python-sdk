# encoding: utf-8


class CxLanguage(object):
    """
    the languages that Checkmarx supported
    """
    def __init__(self, language_id, name):
        """

        Args:
            language_id (int):
            name (str):
        """
        self.id = language_id
        self.name = name

    def __str__(self):
        return "CxLanguage(id={}, name={})".format(
            self.id, self.name
        )
