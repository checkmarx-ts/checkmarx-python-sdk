
class WebError(object):
    def __init__(self, code: int = None, message: str = None, data: dict = None):
        self.code = code
        self.message = message
        self.data = data

    def __str__(self):
        return f"WebError(code={self.code}, message={self.message}, data={self.data})"
