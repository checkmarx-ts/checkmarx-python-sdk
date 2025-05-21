
class SastStatus(object):
    def __init__(self, ready: bool = None, message: str = None):
        self.ready = ready
        self.message = message

    def __str__(self):
        return f"SastStatus(ready={self.ready}, message={self.message})"
