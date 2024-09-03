class CxUserPersistence(object):

    def __init__(self, key, value):
        """

        Args:
            key (str):
            value (str):
        """
        if key and not isinstance(key, str):
            raise ValueError("parameter key should be str")
        if value and not isinstance(value, str):
            raise ValueError("parameter value should be str")
        self.key = key
        self.value = value

    def __str__(self):
        return """CxUserPersistence(key={}, value={})""".format(
            self.key, self.value
        )

    def to_dict(self):
        return {
            "key": self.key,
            "value": self.value,
        }
