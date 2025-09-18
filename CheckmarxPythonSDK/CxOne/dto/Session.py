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


def construct_session(item):
    return Session(
        session_id=item.get("sessionId"),
        tenant_id=item.get("tenantId"),
        project_id=item.get("projectId"),
        source_id=item.get("sourceId"),
        worker_info=WorkerInfo(
            worker_id=item.get("workerInfo").get("worker_id"),
            worker_address=item.get("workerInfo").get("worker_address")
        ),
        status=item.get("status")
    )
