
class RequestStatusNotReady(object):
    def __init__(self, completed: bool = None, value: dict = None):
        self.completed = completed
        self.value = value

    def __str__(self):
        return f"RequestStatusNotReady(completed={self.completed}, value={self.value})"
