# encoding: utf-8


class CxEngineServerStatus(object):
    """
    engine server status
    """

    def __init__(self, status_id=None, value=None):
        """

        Args:
            status_id (int):
            value (str):
        """
        self.id = status_id
        self.value = value

    def __str__(self):
        return "CxEngineServerStatus(id={}, value={})".format(
            self.id, self.value
        )
