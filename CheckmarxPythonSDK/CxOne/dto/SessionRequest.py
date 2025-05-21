
class SessionRequest(object):
    def __init__(self, project_id: str = None, scan_id: str = None, scanner: str = None, timeout: int = None,
                 upload_url: str = None):
        self.projectId = project_id
        self.scanId = scan_id
        self.scanner = scanner
        self.timeout = timeout
        self.uploadUrl = upload_url

    def __str__(self):
        return (f"SessionRequest(projectId={self.projectId}, scanId={self.scanId}, scanner={self.scanner}, "
                f"timeout={self.timeout}, "
                f"uploadUrl={self.uploadUrl})")

    def to_dict(self):
        return {
            "projectId": self.projectId,
            "scanId": self.scanId,
            "scanner": self.scanner,
            "timeout": self.timeout,
            "uploadUrl": self.uploadUrl,
        }
