from dataclasses import dataclass


@dataclass
class Result:
    """

    Attributes:
        type (str): Type of result indicates its engine.
        id (str): ID of the result.
        similarity_id (int): ID of the similarity feature indicates the identification of a result by its first and
                        last nodes.
        status (str): Status enum of a result
        state (str): State enum of a result.
        severity (str): Severity enum of a result.
        confidence_level (int): Confidence level of the exsitence of the result from 0 unknown to 5 high.
        created (str): Creation date of the result.
        first_found_at (str): Date of the first time the result was found.
        found_at (str): Date of finding the result.
        update_at (str): Date of last update of the result.
        first_scan_id (str): ID of the first scan id by resultHash
        description (str): Result query description
        data:
        comments:
        vulnerability_details:

    """
    type: str
    id: str
    similarity_id: int
    status: str
    state: str
    severity: str
    confidence_level: int
    created: str
    first_found_at: str
    found_at: str
    update_at: str
    first_scan_id: str
    description: str
    data: str
    comments: str
    vulnerability_details: str


def construct_result(item):
    return Result(
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
        vulnerability_details=item.get("vulnerabilityDetails")
    )
