
class AuditQuery(object):
    def __init__(self, id: str = None, source: str = None):
        self.id = id
        self.source = source

    def __str__(self):
        return f"AuditQuery(id={self.id}, source={self.source})"

    def to_dict(self):
        return {
            "id": self.id,
            "source": self.source,
        }
