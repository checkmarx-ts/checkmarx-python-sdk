from typing import List


class RequestStatusDetectLanguages(object):
    def __init__(self, completed: bool = None, value: List[str] = None):
        self.completed = completed
        self.value = value

    def __str__(self):
        return f"RequestStatusDetectLanguages(completed={self.completed}, value={self.value})"
