from dataclasses import dataclass
from typing import TypedDict


class WorkerInfo(TypedDict):
    worker_id: str
    worker_address: str


@dataclass
class Session:
    session_id: str = None
    tenant_id: str = None
    project_id: str = None
    source_id: str = None
    worker_info: WorkerInfo = None
    status: int = None

    @classmethod
    def from_dict(cls, item: dict) -> "Session":
        worker_info_data = item.get("workerInfo")
        worker_info = None
        if worker_info_data:
            worker_info = WorkerInfo(
                worker_id=worker_info_data.get("worker_id"),
                worker_address=worker_info_data.get("worker_address"),
            )
        return cls(
            session_id=item.get("sessionId"),
            tenant_id=item.get("tenantId"),
            project_id=item.get("projectId"),
            source_id=item.get("sourceId"),
            worker_info=worker_info,
            status=item.get("status"),
        )
