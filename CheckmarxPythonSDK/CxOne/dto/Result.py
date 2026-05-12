from dataclasses import dataclass


@dataclass
class Result:
    type: str = None
    id: str = None
    similarity_id: int = None
    status: str = None
    state: str = None
    severity: str = None
    confidence_level: int = None
    created: str = None
    first_found_at: str = None
    found_at: str = None
    update_at: str = None
    first_scan_id: str = None
    description: str = None
    data: str = None
    comments: str = None
    vulnerability_details: str = None

    @classmethod
    def from_dict(cls, item: dict) -> "Result":
        return cls(
            type=item.get("type"),
            id=item.get("id"),
            similarity_id=item.get("similarityID"),
            status=item.get("status"),
            state=item.get("state"),
            severity=item.get("severity"),
            confidence_level=item.get("confidenceLevel"),
            created=item.get("created"),
            first_found_at=item.get("firstFoundAt"),
            found_at=item.get("foundAt"),
            update_at=item.get("updateAt"),
            first_scan_id=item.get("firstScanID"),
            description=item.get("description"),
            data=item.get("data"),
            comments=item.get("comments"),
            vulnerability_details=item.get("vulnerabilityDetails"),
        )
