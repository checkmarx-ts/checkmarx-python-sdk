# encoding: utf-8
class StatusDetails(object):
    def __init__(self, name, status, details):
        """

        Args:
            name:
            status:
            details:
        """
        self.name = name
        self.status = status
        self.details = details

    def __str__(self):
        return """StatusDetails(name={}, status={}, details={})""".format(
            self.name, self.status, self.details
        )

    def as_dict(self):
        return {
            "name": self.name,
            "status": self.status,
            "details": self.details
        }
