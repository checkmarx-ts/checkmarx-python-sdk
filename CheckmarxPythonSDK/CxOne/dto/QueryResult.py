
class QueryResult(object):
    def __init__(self, content: str = None, line_number: int = None):
        self.content = content
        self.lineNumber = line_number

    def __str__(self):
        return f"QueryResult(content={self.content}, lineNumber={self.lineNumber})"
