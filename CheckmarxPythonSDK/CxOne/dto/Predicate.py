from dataclasses import dataclass


@dataclass
class Predicate:
    id: str = None
    similarity_id: str = None
    project_id: str = None
    severity: str = None
    state: str = None
    comment: str = None
    created_by: str = None
    created_at: str = None
    change_origin_type: int = None
    change_origin_name: str = None


def construct_predicate(item):
    return Predicate(
        id=item.get("ID"),
        similarity_id=item.get("similarityId"),
        project_id=item.get("projectId"),
        severity=item.get("severity"),
        state=item.get("state"),
        comment=item.get("comment"),
        created_by=item.get("createdBy"),
        created_at=item.get("createdAt"),
        change_origin_type=item.get("changeOriginType"),
        change_origin_name=item.get("changeOriginName")
    )
