class CxEngineServerStatus(object):

    def __init__(self, status_id, value):
        """

        Args:
            status_id (int):
            value (str):
        """
        self.status_id = status_id
        self.value = value

    def __str__(self):
        return """CxEngineServerStatus(status_id={}, value={})""".format(
            self.status_id, self.value
        )
