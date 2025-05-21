
class SessionResponse(object):
    def __init__(self, id: str = None, data: dict = None):
        self.id = id
        self.data = data

    def __str__(self):
        return f"SessionResponse(id={self.id}, data={self.data})"
