from dataclasses import dataclass


@dataclass
class SessionRequest:
    project_id: str
    scan_id: str
    scanner: str = "sast"
    timeout: int = None
    upload_url: str = None

    def to_dict(self):
        data = {
            "projectId": self.project_id,
            "scanId": self.scan_id,
            "scanner": self.scanner,
        }
        if self.timeout:
            data.update({"timeout": self.timeout})
        if self.upload_url:
            data.update({"uploadUrl": self.upload_url})
        return data
