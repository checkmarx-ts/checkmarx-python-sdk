# encoding utf-8
class Flag(object):
    def __init__(self, name, status, payload):
        """

        Args:
            name (str)
            status (boolean)
            payload (dict)
        """
        self.name = name
        self.status = status
        self.payload = payload

    def __str__(self):
        return """Flag(name={name}, status={status}, payload={payload}""".format(
            name=self.name, status=self.status, payload=self.payload
        )
