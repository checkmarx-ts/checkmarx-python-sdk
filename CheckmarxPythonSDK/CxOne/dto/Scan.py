from typing import List
from .StatusDetails import StatusDetails
from dataclasses import dataclass, field


@dataclass
class Scan:
    id: str = None
    status: str = None
    status_details: List[StatusDetails] = field(default_factory=list)
    position_in_queue: int = None
    project_id: str = None
    project_name: str = None
    branch: str = None
    commit_id: str = None
    commit_tag: str = None
    upload_url: str = None
    created_at: str = None
    updated_at: str = None
    user_agent: str = None
    initiator: str = None
    tags: dict = None
    metadata: dict = None
    engines: List[str] = None
    source_type: str = None
    source_origin: str = None

    @classmethod
    def from_dict(cls, item: dict) -> "Scan":
        return cls(
            id=item.get("id"),
            status=item.get("status"),
            status_details=[
                StatusDetails.from_dict(d) for d in (item.get("statusDetails") or [])
            ],
            position_in_queue=item.get("positionInQueue"),
            project_id=item.get("projectId"),
            project_name=item.get("projectName"),
            branch=item.get("branch"),
            commit_id=item.get("commitId"),
            commit_tag=item.get("commitTag"),
            upload_url=item.get("uploadUrl"),
            created_at=item.get("createdAt"),
            updated_at=item.get("updatedAt"),
            user_agent=item.get("userAgent"),
            initiator=item.get("initiator"),
            tags=item.get("tags"),
            metadata=item.get("metadata"),
            engines=item.get("engines"),
            source_type=item.get("sourceType"),
            source_origin=item.get("sourceOrigin"),
        )
