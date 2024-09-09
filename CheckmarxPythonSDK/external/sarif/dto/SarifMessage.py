class SarifMessage:
    def __init__(self, text):
        """

        Args:
            text (str):
        """
        self.text = text

    def __str__(self):
        return f"SarifMessage(" \
               f"text={self.text}"\
               f")"
