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

    def __eq__(self, other):

        return (self.name == other.name and
                self.status == other.status and
                self.payload == other.payload)

    def __lt__(self, other):

        return self.name < other.name

    def __str__(self):
        return """Flag(name={name}, status={status}, payload={payload})""".format(
            name=self.name, status=self.status, payload=self.payload
        )
