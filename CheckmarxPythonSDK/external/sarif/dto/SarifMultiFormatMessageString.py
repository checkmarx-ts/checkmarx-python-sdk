class SarifMultiFormatMessageString(object):

    def __init__(self, general, text, markdown):
        """

        Args:
            general (str):
            text (str):
            markdown (str):
        """
        self.general = general
        self.text = text
        self.markdown = markdown

    def __str__(self):
        return f"""SarifMultiFormatMessageString(
        general={self.general}, 
        text={self.text}, 
        markdown={self.markdown})
        """
