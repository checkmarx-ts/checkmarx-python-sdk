class SarifMessage:
    def __init__(self, text):
        """

        Args:
            text (str):
        """
        self.Text = text

    def __str__(self):
        return f"SarifMessage(" \
               f"text={self.Text}"\
               f")"
