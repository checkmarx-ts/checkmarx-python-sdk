class CxSASTConfig(object):

    def __init__(self, key, value, description=None):
        """

        Args:
            key (str):
            value (str):
            description (str):
        """
        self.key = key
        self.value = value
        self.description = description

    def get_key_value_dict(self):
        return {
            "key": self.key,
            "value": self.value
        }

    def __str__(self):
        return """CxSASTConfig(key={key}, value={value}, description={description})""".format(
            key=self.key, value=self.value, description=self.description
        )
