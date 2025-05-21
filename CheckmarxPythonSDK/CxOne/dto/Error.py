
class Error(object):
    def __init__(self, code: int = None, message: str = None):
        self.code = code
        self.message = message

    def __str__(self):
        return f"Error(code={self.code}, message={self.message})"
