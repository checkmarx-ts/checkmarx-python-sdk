# encoding: utf-8


class CxOsaState(object):
    """
    state
    """
    def __init__(self, state_id, name, failure_reason):
        """

        Args:
            state_id (int):
            name (str):
            failure_reason (int):
        """
        self.id = state_id
        self.name = name
        self.failure_reason = failure_reason

    def __str__(self):
        return """CxOsaState(id={}, name={}, failure_reason={})""".format(
            self.id, self.name, self.failure_reason
        )
