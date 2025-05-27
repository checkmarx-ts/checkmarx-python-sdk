
class SessionRequest(object):
    def __init__(self, project_id: str, scan_id: str, scanner: str = "sast", timeout: int = None,
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
        data = {
            "projectId": self.projectId,
            "scanId": self.scanId,
            "scanner": self.scanner,
        }
        if self.timeout:
            data.update({"timeout": self.timeout})
        if self.uploadUrl:
            data.update({"uploadUrl": self.uploadUrl})
        return data
