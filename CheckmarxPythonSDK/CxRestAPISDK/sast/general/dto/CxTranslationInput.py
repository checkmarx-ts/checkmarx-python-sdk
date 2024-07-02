class CxTranslationInput(object):
    """
        One language translation of a result state
    """
    def __init__(self, language_id, name):
        self.language_id = language_id
        self.name = name

    def __str__(self):
        return """CxTranslationInput(language_id={}, name={})""".format(
            self.language_id, self.name
        )

    def to_dict(self):
        return {
            "languageId": self.language_id,
            "name": self.name
        }
