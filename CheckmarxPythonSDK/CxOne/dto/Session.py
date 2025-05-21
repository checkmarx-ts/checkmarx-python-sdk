from typing import TypedDict


class WorkerInfo(TypedDict):
    worker_id: str
    worker_address: str


class Session(object):
    def __init__(self, session_id: str = None, tenant_id: str = None, project_id: str = None, source_id: str = None,
                 worker_info: WorkerInfo = None, status: int = None):
        self.session_id = session_id
        self.tenant_id = tenant_id
        self.project_id = project_id
        self.source_id = source_id
        self.worker_info = worker_info
        self.status = status

    def __str__(self):
        return (f"Session(session_id={self.session_id}, tenant_id={self.tenant_id}, project_id={self.project_id}, "
                f"source_id={self.source_id}, worker_info={self.worker_info}, status={self.status})")
