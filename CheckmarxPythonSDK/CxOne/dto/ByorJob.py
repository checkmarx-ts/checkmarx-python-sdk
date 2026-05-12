from dataclasses import dataclass


@dataclass
class ByorJob:
    id: str = None
    project_id: str = None
    status: str = None
    percentage: str = None
    error: str = None

    @classmethod
    def from_dict(cls, item: dict) -> "ByorJob":
        return cls(
            id=item.get("id"),
            project_id=item.get("projectId"),
            status=item.get("status"),
            percentage=item.get("percentage"),
            error=item.get("error"),
        )
