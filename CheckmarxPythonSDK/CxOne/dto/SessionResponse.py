
class SessionResponse(object):
    def __init__(self, id: str = None, status: str = None, scan_id: str = None):
        self.id = id
        self.status = status
        self.scanId = scan_id

    def __str__(self):
        return f"SessionResponse(id={self.id}, status={self.status}, scanId={self.scanId})"
