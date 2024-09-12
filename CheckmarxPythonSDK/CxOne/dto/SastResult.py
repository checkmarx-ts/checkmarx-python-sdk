from .ResultNode import ResultNode, construct_result_node
from .ChangeDetails import ChangeDetails, construct_change_details


class SastResult(object):
    def __init__(self, result_id, result_hash=None, query_id=None, query_id_str=None,
                 query_name=None, language_name=None,
                 query_group=None, cwe_id=None, severity=None, similarity_id=None, confidence_level=None,
                 compliances=None, first_scan_id=None, first_found_at=None,
                 path_system_id_by_simi_and_files_paths=None, status=None, found_at=None, nodes=None,
                 state=None, change_details=None):
        """

        Args:
            result_id (str): ID of the result
            result_hash (str): ID of the path id system wide
            query_id (int): Query ID
            query_id_str (str): The ID of the query that generated this result in string format (i.e. the vulnerability that was identified)
            query_name (str): Query name
            language_name (str): Language name
            query_group (str): Query group name
            cwe_id (int): Query Common Weakness Enumeration ID
            severity (str): Severity enum of a result.
                            Enum:
                            [ HIGH, MEDIUM, LOW, INFO ]
            similarity_id (int): ID of the Similarity feature (Indicator to identify a result by its
                            first and last nodes)
            confidence_level (int): Confidence Level of the exsiting of the result
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
        self.result_id = result_id
        self.result_hash = result_hash
        self.query_id = query_id
        self.query_id_str = query_id_str
        self.query_name = query_name
        self.language_name = language_name
        self.query_group = query_group
        self.cwe_id = cwe_id
        self.severity = severity
        self.similarity_id = similarity_id
        self.confidence_level = confidence_level
        self.compliances = compliances
        self.first_scan_id = first_scan_id
        self.first_found_at = first_found_at
        self.path_system_id_by_simi_and_files_paths = path_system_id_by_simi_and_files_paths
        self.status = status
        self.found_at = found_at
        self.nodes = nodes
        self.state = state
        self.change_details = change_details

    def __str__(self):
        return f"""SastResult(
        result_id={self.result_id}, 
        result_hash={self.result_hash}, 
        query_id={self.query_id}, 
        query_id_str={self.query_id_str}, 
        query_name={self.query_name}, 
        language_name={self.language_name}, 
        query_group={self.query_group}, 
        cwe_id={self.cwe_id}, 
        severity={self.severity}, 
        similarity_id={self.similarity_id}, 
        confidence_level={self.confidence_level}, 
        compliances={self.compliances}, 
        first_scan_id={self.first_scan_id}, 
        first_found_at={self.first_found_at}, 
        path_system_id_by_simi_and_files_paths={self.path_system_id_by_simi_and_files_paths}, 
        status={self.status}, 
        found_at={self.found_at}, 
        nodes={self.nodes}, 
        state={self.state},
        change_details={self.change_details},
        )"""


def construct_sast_result(result):
    return SastResult(
        result_id=result.get('resultHash'),
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
            construct_result_node(node) for node in result.get("nodes") or []
        ],
        state=result.get("state"),
        change_details=construct_change_details(result.get("changeDetails"))
    )
