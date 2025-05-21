
class AsyncRequestResponse(object):
    def __init__(self, id: str = None):
        self.id = id

    def __str__(self):
        return f"AsyncRequestResponse(id={self.id})"

    def to_dict(self):
        return {
            "id": self.id
        }
