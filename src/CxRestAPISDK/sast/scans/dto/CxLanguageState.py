# encoding: utf-8


class CxLanguageState(object):
    """
    language state
    """

    def __init__(self, language_id, language_name, language_hash, state_creation_date):
        """

        Args:
            language_id (int):
            language_name (str):
            language_hash (str):
            state_creation_date (str):
        """
        self.language_id = language_id
        self.language_name = language_name
        self.language_hash = language_hash
        self.state_creation_date = state_creation_date

    def __str__(self):
        return "LanguageState(language_id={}, language_name={}, language_hash={}, state_creation_date={})".format(
            self.language_id, self.language_name, self.language_hash, self.state_creation_date
        )
