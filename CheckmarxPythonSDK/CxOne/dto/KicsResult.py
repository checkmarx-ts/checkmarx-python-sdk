from dataclasses import dataclass


@dataclass
class KicsResult:
    kics_result_id: str = None
    similarity_id: int = None
    severity: str = None
    first_scan_id: str = None
    first_found_at: str = None
    found_at: str = None
    status: str = None
    state: str = None
    kics_type: str = None
    query_id: int = None
    query_name: str = None
    query_group: str = None
    query_url: str = None
    file_name: str = None
    line: int = None
    platform: str = None
    issue_type: str = None
    search_key: str = None
    search_value: str = None
    expected_value: str = None
    actual_value: str = None
    value: str = None
    description: str = None
    comments: str = None
    category: str = None

    @classmethod
    def from_dict(cls, item: dict) -> "KicsResult":
        return cls(
            kics_result_id=item.get("ID"),
            similarity_id=item.get("similarityID"),
            severity=item.get("severity"),
            first_scan_id=item.get("firstScanID"),
            first_found_at=item.get("firstFoundAt"),
            found_at=item.get("foundAt"),
            status=item.get("status"),
            state=item.get("state"),
            kics_type=item.get("type"),
            query_id=item.get("queryID"),
            query_name=item.get("queryName"),
            query_group=item.get("group"),
            query_url=item.get("queryUrl"),
            file_name=item.get("fileName"),
            line=item.get("line"),
            platform=item.get("platform"),
            issue_type=item.get("issueType"),
            search_key=item.get("searchKey"),
            search_value=item.get("searchValue"),
            expected_value=item.get("expectedValue"),
            actual_value=item.get("actualValue"),
            value=item.get("value"),
            description=item.get("description"),
            comments=item.get("comments"),
            category=item.get("category"),
        )
