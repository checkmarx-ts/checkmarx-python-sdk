class CxSASTConfig(object):

    def __init__(self, key, value, description):
        """

        Args:
            key (str):
            value (str):
            description (str):
        """
        self.key = key
        self.value = value
        self.description = description

    def __str__(self):
        return """CxSASTConfig(key={key}, value={value}, description={description})""".format(
            key=self.key, value=self.value, description=self.description
        )
