from dataclasses import dataclass
from typing import List
from .ResultNode import ResultNode
from .ChangeDetails import ChangeDetails


@dataclass
class SastResult:
    id: str = None
    result_hash: str = None
    query_id: int = None
    query_id_str: str = None
    query_name: str = None
    language_name: str = None
    query_group: str = None
    cwe_id: int = None
    severity: str = None
    similarity_id: int = None
    confidence_level: int = None
    compliances: List[str] = None
    first_scan_id: str = None
    first_found_at: str = None
    path_system_id_by_simi_and_files_paths: str = None
    status: str = None
    found_at: str = None
    nodes: List[ResultNode] = None
    state: str = None
    change_details: ChangeDetails = None

    @classmethod
    def from_dict(cls, item: dict) -> "SastResult":
        return cls(
            id=item.get("resultHash"),
            result_hash=item.get("resultHash"),
            query_id=item.get("queryID"),
            query_id_str=item.get("queryIDStr"),
            query_name=item.get("queryName"),
            language_name=item.get("languageName"),
            query_group=item.get("group"),
            cwe_id=item.get("cweID"),
            severity=item.get("severity"),
            similarity_id=item.get("similarityID"),
            confidence_level=item.get("confidenceLevel"),
            compliances=item.get("compliances"),
            first_scan_id=item.get("firstScanID"),
            first_found_at=item.get("firstFoundAt"),
            path_system_id_by_simi_and_files_paths=item.get("pathSystemID"),
            status=item.get("status"),
            found_at=item.get("foundAt"),
            nodes=[ResultNode.from_dict(node) for node in (item.get("nodes") or [])],
            state=item.get("state"),
            change_details=ChangeDetails.from_dict(item.get("changeDetails")),
        )
