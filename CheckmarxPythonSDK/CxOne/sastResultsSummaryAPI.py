from CheckmarxPythonSDK.api_client import ApiClient
from CheckmarxPythonSDK.CxOne.config import construct_configuration
from typing import List
from .utilities import type_check, list_member_type_check

api_url = "/api/sast-scan-summary"


class SastResultsSummaryAPI(object):

    def __init__(self, api_client: ApiClient = None):
        if api_client is None:
            configuration = construct_configuration()
            api_client = ApiClient(configuration=configuration)
        self.api_client = api_client

    def get_sast_aggregate_results(
            self, scan_id: str, group_by_field: List[str], language: List[str] = None, status: List[str] = None,
            severity: List[str] = None, source_file: str = None, source_file_operation: str = None,
            source_node: str = None, source_node_operation: str = None, sink_node: str = None,
            sink_node_operation: str = None, sink_file: str = None, sink_file_operation: str = None,
            query_ids: List[int] = None, apply_predicates: bool = True, limit: int = 20, offset: int = 0
    ) -> dict:
        """

        Args:
            scan_id (str): filter by scan id
            group_by_field (list of str): fields to group results
                    Available values : QUERY, SEVERITY, STATUS, SOURCE_NODE, SINK_NODE, SOURCE_FILE, SINK_FILE, LANGUAGE
            language (list of str): filter by language name. matching languages that EQUALS the input with
                                    case-insensitive.
            status (list of str): filter by status. OR operator between the items.
                            Available values : NEW, RECURRENT
            severity (list of str): filter by severity. OR operator between the items.
                            Available values : HIGH, MEDIUM, LOW, INFO
            source_file (str): filter by source file name
            source_file_operation (str): filter operation for source file
                            Available values : CONTAINS, EQUAL
            source_node (str): filter by source node
            source_node_operation (str): filter operation for source node
                            Available values : CONTAINS, EQUAL
            sink_node (str): filter by sink node
            sink_node_operation (str): filter operation for sink node
                            Available values : CONTAINS, EQUAL
            sink_file (str): filter by sink file name
            sink_file_operation (str): filter operation for sink file
                            Available values : CONTAINS, EQUAL
            query_ids (list of int): filter by queries ids
            apply_predicates (bool): if true will apply changes from predicates, otherwise will return the raw results
                            summary. Default value : true
            limit (int): limit results numbers Default value : 20
            offset (int): offset results Default value : 0

        Returns:
            dict
        """
        type_check(scan_id, str)
        type_check(group_by_field, (list, tuple))
        type_check(language, (list, tuple))
        type_check(status, (list, tuple))
        type_check(severity, (list, tuple))
        type_check(source_file, str)
        type_check(source_file_operation, str)
        type_check(source_node, str)
        type_check(source_node_operation, str)
        type_check(sink_node, str)
        type_check(sink_node_operation, str)
        type_check(sink_file, str)
        type_check(sink_file_operation, str)
        type_check(query_ids, (list, tuple))
        type_check(apply_predicates, bool)
        type_check(limit, int)
        type_check(offset, int)

        list_member_type_check(group_by_field, str)
        list_member_type_check(language, str)
        list_member_type_check(status, str)
        list_member_type_check(severity, str)
        list_member_type_check(query_ids, int)

        relative_url = api_url + "/aggregate"
        params = {
            "scan-id": scan_id, "group-by-field": group_by_field, "language": language, "status": status,
            "severity": severity,
            "source-file": source_file, "source-file-operation": source_file_operation,
            "source-node": source_node, "source-node-operation": source_node_operation,
            "sink-node": sink_node, "sink-node-operation": sink_node_operation,
            "sink-file": sink_file, "sink-file-operation": sink_file_operation,
            "query-ids": query_ids, "apply-predicates": apply_predicates,
            "limit": limit, "offset": offset
        }
        response = self.api_client.get_request(relative_url=relative_url, params=params)
        return response.json()

    def get_sast_aggregate_results_comparison(
            self, scan_id: str, base_scan_id: str, group_by_field: List[str], language: List[str] = None,
            status: List[str] = None, severity: List[str] = None, query_ids: List[int] = None,
            limit: int = 20, offset: int = 0
    ) -> dict:
        """

        Args:
            scan_id (str):  Scan ID of the newer scan to compare
            base_scan_id (str):  Scan ID of the older scan to compare
            group_by_field (List[str]):  Specify parameters for grouping results Available values : LANGUAGE, QUERY
            language (List[str]):  Filter results by language Note: Exact match, case-insensitive.
            status (List[str]):  Filter results by status Available values : NEW, RECURRENT, FIXED
            severity (List[str]):  Filter results by severity  Available values : CRITICAL, HIGH, MEDIUM, LOW, INFO
            query_ids (List[int]):  Filter results by query IDs
            limit (int):  The maximum number of results to return Default value : 20
            offset (int):  The number of results to skip before returning results Default value : 0

        Returns:
            dict
        """
        relative_url = api_url + "/compare/aggregate"
        params = {
            "scan-id": scan_id, "base-scan-id": base_scan_id, "group-by-field": group_by_field,
            "language": language, "status": status, "severity": severity, "query-ids": query_ids,
            "limit": limit, "offset": offset,
        }
        response = self.api_client.get_request(relative_url=relative_url, params=params)
        return response.json()


def get_sast_aggregate_results(
        scan_id: str, group_by_field: List[str], language: List[str] = None, status: List[str] = None,
        severity: List[str] = None, source_file: str = None, source_file_operation: str = None,
        source_node: str = None, source_node_operation: str = None, sink_node: str = None,
        sink_node_operation: str = None, sink_file: str = None, sink_file_operation: str = None,
        query_ids: List[int] = None, apply_predicates: bool = True, limit: int = 20, offset: int = 0
) -> dict:
    return SastResultsSummaryAPI().get_sast_aggregate_results(
        scan_id=scan_id, group_by_field=group_by_field, language=language, status=status, severity=severity,
        source_file=source_file, source_file_operation=source_file_operation, source_node=source_node,
        source_node_operation=source_node_operation, sink_node=sink_node, sink_node_operation=sink_node_operation,
        sink_file=sink_file, sink_file_operation=sink_file_operation, query_ids=query_ids,
        apply_predicates=apply_predicates, limit=limit, offset=offset
    )


def get_sast_aggregate_results_comparison(
        scan_id: str, base_scan_id: str, group_by_field: List[str], language: List[str] = None,
        status: List[str] = None, severity: List[str] = None, query_ids: List[int] = None,
        limit: int = 20, offset: int = 0
) -> dict:
    return SastResultsSummaryAPI().get_sast_aggregate_results_comparison(
        scan_id=scan_id, base_scan_id=base_scan_id, group_by_field=group_by_field, language=language,
        status=status, severity=severity, query_ids=query_ids, limit=limit, offset=offset,
    )
