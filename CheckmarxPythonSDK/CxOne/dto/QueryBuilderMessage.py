
class QueryBuilderMessage(object):
    def __init__(self, role: str = None, content: str = None):
        self.role = role
        self.content = content

    def __str__(self):
        return f"QueryBuilderMessage(role={self.role}, content={self.content})"
