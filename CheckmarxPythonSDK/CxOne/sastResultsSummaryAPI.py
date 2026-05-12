from CheckmarxPythonSDK.api_client import ApiClient
from CheckmarxPythonSDK.CxOne.config import construct_configuration
from typing import List


class SastResultsSummaryAPI(object):

    def __init__(self, api_client: ApiClient = None):
        if api_client is None:
            configuration = construct_configuration()
            api_client = ApiClient(configuration=configuration)
        self.api_client = api_client
        self.base_url = (
            f"{self.api_client.configuration.server_base_url}"
            f"/api/sast-scan-summary"
        )

    def get_sast_aggregate_results(
        self,
        scan_id: str,
        group_by_field: List[str],
        language: List[str] = None,
        status: List[str] = None,
        severity: List[str] = None,
        source_file: str = None,
        source_file_operation: str = None,
        source_node: str = None,
        source_node_operation: str = None,
        sink_node: str = None,
        sink_node_operation: str = None,
        sink_file: str = None,
        sink_file_operation: str = None,
        query_ids: List[int] = None,
        apply_predicates: bool = True,
        limit: int = 20,
        offset: int = 0,
    ) -> dict:
        """
        Args:
            scan_id (str): Filter by scan id.
            group_by_field (list of str): Fields to group results.
                Values: QUERY, SEVERITY, STATUS, SOURCE_NODE, SINK_NODE,
                SOURCE_FILE, SINK_FILE, LANGUAGE
            language (list of str): Filter by language (case-insensitive,
                exact match).
            status (list of str): Filter by status (OR between items).
                Values: NEW, RECURRENT
            severity (list of str): Filter by severity (OR between items).
                Values: HIGH, MEDIUM, LOW, INFO
            source_file (str): Filter by source file name.
            source_file_operation (str): Operation for source file.
                Values: CONTAINS, EQUAL
            source_node (str): Filter by source node.
            source_node_operation (str): Operation for source node.
                Values: CONTAINS, EQUAL
            sink_node (str): Filter by sink node.
            sink_node_operation (str): Operation for sink node.
                Values: CONTAINS, EQUAL
            sink_file (str): Filter by sink file name.
            sink_file_operation (str): Operation for sink file.
                Values: CONTAINS, EQUAL
            query_ids (list of int): Filter by query ids.
            apply_predicates (bool): Apply predicate changes. Default: true.
            limit (int): Limit results. Default: 20.
            offset (int): Offset results. Default: 0.

        Returns:
            dict
        """
        url = f"{self.base_url}/aggregate"
        params = {
            "scan-id": scan_id,
            "group-by-field": group_by_field,
            "language": language,
            "status": status,
            "severity": severity,
            "source-file": source_file,
            "source-file-operation": source_file_operation,
            "source-node": source_node,
            "source-node-operation": source_node_operation,
            "sink-node": sink_node,
            "sink-node-operation": sink_node_operation,
            "sink-file": sink_file,
            "sink-file-operation": sink_file_operation,
            "query-ids": query_ids,
            "apply-predicates": apply_predicates,
            "limit": limit,
            "offset": offset,
        }
        response = self.api_client.call_api(
            method="GET", url=url, params=params
        )
        return response.json()

    def get_sast_aggregate_results_comparison(
        self,
        scan_id: str,
        base_scan_id: str,
        group_by_field: List[str],
        language: List[str] = None,
        status: List[str] = None,
        severity: List[str] = None,
        query_ids: List[int] = None,
        limit: int = 20,
        offset: int = 0,
    ) -> dict:
        """
        Args:
            scan_id (str): Scan ID of the newer scan to compare.
            base_scan_id (str): Scan ID of the older scan to compare.
            group_by_field (List[str]): Group by parameters.
                Values: LANGUAGE, QUERY
            language (List[str]): Filter by language (exact,
                case-insensitive).
            status (List[str]): Filter by status.
                Values: NEW, RECURRENT, FIXED
            severity (List[str]): Filter by severity.
                Values: CRITICAL, HIGH, MEDIUM, LOW, INFO
            query_ids (List[int]): Filter by query IDs.
            limit (int): Maximum results. Default: 20.
            offset (int): Results to skip. Default: 0.

        Returns:
            dict
        """
        url = f"{self.base_url}/compare/aggregate"
        params = {
            "scan-id": scan_id,
            "base-scan-id": base_scan_id,
            "group-by-field": group_by_field,
            "language": language,
            "status": status,
            "severity": severity,
            "query-ids": query_ids,
            "limit": limit,
            "offset": offset,
        }
        response = self.api_client.call_api(
            method="GET", url=url, params=params
        )
        return response.json()


def get_sast_aggregate_results(
    scan_id: str,
    group_by_field: List[str],
    language: List[str] = None,
    status: List[str] = None,
    severity: List[str] = None,
    source_file: str = None,
    source_file_operation: str = None,
    source_node: str = None,
    source_node_operation: str = None,
    sink_node: str = None,
    sink_node_operation: str = None,
    sink_file: str = None,
    sink_file_operation: str = None,
    query_ids: List[int] = None,
    apply_predicates: bool = True,
    limit: int = 20,
    offset: int = 0,
) -> dict:
    return SastResultsSummaryAPI().get_sast_aggregate_results(
        scan_id=scan_id,
        group_by_field=group_by_field,
        language=language,
        status=status,
        severity=severity,
        source_file=source_file,
        source_file_operation=source_file_operation,
        source_node=source_node,
        source_node_operation=source_node_operation,
        sink_node=sink_node,
        sink_node_operation=sink_node_operation,
        sink_file=sink_file,
        sink_file_operation=sink_file_operation,
        query_ids=query_ids,
        apply_predicates=apply_predicates,
        limit=limit,
        offset=offset,
    )


def get_sast_aggregate_results_comparison(
    scan_id: str,
    base_scan_id: str,
    group_by_field: List[str],
    language: List[str] = None,
    status: List[str] = None,
    severity: List[str] = None,
    query_ids: List[int] = None,
    limit: int = 20,
    offset: int = 0,
) -> dict:
    return SastResultsSummaryAPI().get_sast_aggregate_results_comparison(
        scan_id=scan_id,
        base_scan_id=base_scan_id,
        group_by_field=group_by_field,
        language=language,
        status=status,
        severity=severity,
        query_ids=query_ids,
        limit=limit,
        offset=offset,
    )
