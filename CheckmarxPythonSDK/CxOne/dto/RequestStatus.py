from .CompilationResponse import CompilationResponse
from .ExecutionResponse import ExecutionResponse


class RequestStatus(object):
    def __init__(self, completed: bool = None, status: str = None, value=None):
        self.completed = completed
        self.status = status
        self.value = value

    def __str__(self):
        return f"RequestStatus(completed={self.completed}, status={self.status}, value={self.value})"
