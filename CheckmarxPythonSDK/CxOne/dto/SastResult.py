from dataclasses import dataclass
from typing import List
from .ResultNode import ResultNode, construct_result_node
from .ChangeDetails import ChangeDetails, construct_change_details


@dataclass
class SastResult:
    """

    Attributes:
        id (str): ID of the result
        result_hash (str): ID of the path id system wide
        query_id (int): Query ID
        query_id_str (str): The ID of the query that generated this result in string format (i.e. the vulnerability that
                            was identified)
        query_name (str): Query name
        language_name (str): Language name
        query_group (str): Query group name
        cwe_id (int): Query Common Weakness Enumeration ID
        severity (str): Severity enum of a result.
                        Enum:
                        [ HIGH, MEDIUM, LOW, INFO ]
        similarity_id (int): ID of the Similarity feature (Indicator to identify a result by its
                        first and last nodes)
        confidence_level (int): Confidence Level of the existing of the result
        compliances (list of str):
        first_scan_id (str): ID of the first scan id by resultHash
        first_found_at (str): date of the first found by resultHash
        path_system_id_by_simi_and_files_paths (str): ID created from queryMetaInfo + similarityID + files name.
        status (str): Status enum of a result
                    Enum:
                    [ NEW, RECURRENT, FIXED ]
        found_at (str): Creation date of the result
        nodes (list of ResultNode): array of the nodes. will be included only if the include-nodes parameter is true
        state (str): TO_VERIFY, NOT_EXPLOITABLE, PROPOSED_NOT_EXPLOITABLE, CONFIRMED, URGENT
        change_details (ChangeDetails)
    """

    id: str
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


def construct_sast_result(result):
    return SastResult(
        id=result.get('resultHash'),
        result_hash=result.get("resultHash"),
        query_id=result.get("queryID"),
        query_id_str=result.get("queryIDStr"),
        query_name=result.get("queryName"),
        language_name=result.get("languageName"),
        query_group=result.get("group"),
        cwe_id=result.get("cweID"),
        severity=result.get("severity"),
        similarity_id=result.get("similarityID"),
        confidence_level=result.get("confidenceLevel"),
        compliances=result.get("compliances"),
        first_scan_id=result.get("firstScanID"),
        first_found_at=result.get("firstFoundAt"),
        path_system_id_by_simi_and_files_paths=result.get('pathSystemID'),
        status=result.get("status"),
        found_at=result.get("foundAt"),
        nodes=[
            construct_result_node(node) for node in result.get("nodes", [])
        ],
        state=result.get("state"),
        change_details=construct_change_details(result.get("changeDetails"))
    )
