from CheckmarxPythonSDK.api_client import ApiClient
from CheckmarxPythonSDK.CxOne.config import construct_configuration
from typing import List
from .dto import SastResult


class SastResultsAPI(object):

    def __init__(self, api_client: ApiClient = None):
        if api_client is None:
            configuration = construct_configuration()
            api_client = ApiClient(configuration=configuration)
        self.api_client = api_client
        self.base_url = (
            f"{self.api_client.configuration.server_base_url}/api/sast-results"
        )

    def get_sast_results_by_scan_id(
        self,
        scan_id: str,
        severity: List[str] = None,
        state: List[str] = None,
        status: List[str] = None,
        query_group: str = None,
        compliance: str = None,
        query: str = None,
        language: List[str] = None,
        query_ids: List[str] = None,
        node_ids: List[str] = None,
        source_file: str = None,
        source_file_operation: str = None,
        source_node: str = None,
        source_node_operation: str = None,
        source_line: int = None,
        source_line_operation: str = None,
        sink_node: str = None,
        sink_node_operation: str = None,
        sink_file: str = None,
        sink_file_operation: str = None,
        sink_line: int = None,
        sink_line_operation: str = None,
        number_of_nodes: int = None,
        number_of_nodes_operation: str = None,
        notes: str = None,
        notes_operation: str = None,
        first_found_at: str = None,
        first_found_at_operation: str = None,
        preset_id: str = None,
        result_id: List[str] = None,
        category: str = None,
        search: str = None,
        include_nodes: bool = True,
        apply_predicates: bool = True,
        offset: int = 0,
        limit: int = 20,
        sort: List[str] = ("+status", "+severity", "-queryname"),
    ) -> dict:
        """
        Args:
            scan_id (str): Filter by scan id.
            severity (list of str): Filter by severity. OR between items.
                Available values: CRITICAL, HIGH, MEDIUM, LOW, INFO
            state (list of str): TO_VERIFY, NOT_EXPLOITABLE,
                PROPOSED_NOT_EXPLOITABLE, CONFIRMED, URGENT
            status (list of str): Filter by status. OR between items.
                Available values: NEW, RECURRENT, FIXED
            query_group (str): Filter by vulnerability group (substring).
            compliance (str): Filter by compliance standard (exact,
                case-insensitive).
            query (str): Filter by query (exact match).
            language (list of str): Filter by language (exact,
                case-insensitive).
            query_ids (list of str): Filter by query ids (exact match).
            node_ids (list of str): Filter by Node IDs (OR for multiple).
            source_file (str): Filter by source file name.
            source_file_operation (str): Operation for source file filter.
                Values: LESS_THAN, GREATER_THAN, CONTAINS, NOT_CONTAINS,
                EQUAL, NOT_EQUAL, START_WITH
            source_node (str): Filter by source node.
            source_node_operation (str): Operation for source node filter.
                Values: LESS_THAN, GREATER_THAN, CONTAINS, NOT_CONTAINS,
                EQUAL, NOT_EQUAL, START_WITH
            source_line (int): Filter by source line.
            source_line_operation (str): Operation for source line filter.
                Values: LESS_THAN, GREATER_THAN, EQUAL, NOT_EQUAL
            sink_node (str): Filter by sink node.
            sink_node_operation (str): Operation for sink node filter.
                Values: LESS_THAN, GREATER_THAN, CONTAINS, NOT_CONTAINS,
                EQUAL, NOT_EQUAL, START_WITH
            sink_file (str): Filter by sink file name.
            sink_file_operation (str): Operation for sink file filter.
                Values: LESS_THAN, GREATER_THAN, CONTAINS, NOT_CONTAINS,
                EQUAL, NOT_EQUAL, START_WITH
            sink_line (int): Filter by sink line.
            sink_line_operation (str): Operation for sink line filter.
            number_of_nodes (int): Filter by number of nodes.
            number_of_nodes_operation (str): Operation for nodes filter.
                Values: LESS_THAN, GREATER_THAN, EQUAL, NOT_EQUAL
            notes (str): Filter by last notes.
            notes_operation (str): Operation for notes filter.
                Values: CONTAINS, START_WITH
            first_found_at (str): Filter by first found at.
            first_found_at_operation (str): Operation for first found at.
                Default: GREATER_THAN. Values: LESS_THAN, GREATER_THAN
            preset_id (str): Filter by preset.
            result_id (list of str): Filter by unique result hash.
            category (str): Filter by category name.
            search (str): Filter by source file, source/sink node, notes.
            include_nodes (bool): Return ResultNode objects. Default: true.
            apply_predicates (bool): Apply predicate changes. Default: true.
            offset (int): Items to skip. Default: 0.
            limit (int): Items to return. Default: 20.
            sort (list of str): Ordered sort array, each "[-+]field".
                Values: severity, status, firstfoundat, foundat,
                queryname, firstscanid

        Returns:
            dict
        """
        params = {
            "scan-id": scan_id,
            "severity": severity,
            "state": state,
            "status": status,
            "group": query_group,
            "compliance": compliance,
            "query": query,
            "language": language,
            "query-ids": query_ids,
            "node-ids": node_ids,
            "source-file": source_file,
            "source-file-operation": source_file_operation,
            "source-node": source_node,
            "source-node-operation": source_node_operation,
            "source-line": source_line,
            "source-line-operation": source_line_operation,
            "sink-node": sink_node,
            "sink-node-operation": sink_node_operation,
            "sink-file": sink_file,
            "sink-file-operation": sink_file_operation,
            "sink-line": sink_line,
            "sink-line-operation": sink_line_operation,
            "number-of-nodes": number_of_nodes,
            "number-of-nodes-operation": number_of_nodes_operation,
            "notes": notes,
            "notes-operation": notes_operation,
            "first-found-at": first_found_at,
            "first-found-at-operation": first_found_at_operation,
            "preset-id": preset_id,
            "result-id": result_id,
            "category": category,
            "search": search,
            "include-nodes": include_nodes,
            "apply-predicates": apply_predicates,
            "offset": offset,
            "limit": limit,
            "sort": ",".join(sort) if sort else None,
        }
        response = self.api_client.call_api(
            method="GET", url=self.base_url, params=params
        )
        resp = response.json()
        return {
            "results": [
                SastResult.from_dict(r)
                for r in (resp.get("results") or [])
            ],
            "totalCount": resp.get("totalCount"),
        }


def get_sast_results_by_scan_id(
    scan_id: str,
    severity: List[str] = None,
    state: List[str] = None,
    status: List[str] = None,
    query_group: str = None,
    compliance: str = None,
    query: str = None,
    language: List[str] = None,
    query_ids: List[str] = None,
    node_ids: List[str] = None,
    source_file: str = None,
    source_file_operation: str = None,
    source_node: str = None,
    source_node_operation: str = None,
    source_line: int = None,
    source_line_operation: str = None,
    sink_node: str = None,
    sink_node_operation: str = None,
    sink_file: str = None,
    sink_file_operation: str = None,
    sink_line: int = None,
    sink_line_operation: str = None,
    number_of_nodes: int = None,
    number_of_nodes_operation: str = None,
    notes: str = None,
    notes_operation: str = None,
    first_found_at: str = None,
    first_found_at_operation: str = None,
    preset_id: str = None,
    result_id: List[str] = None,
    category: str = None,
    search: str = None,
    include_nodes: bool = True,
    apply_predicates: bool = True,
    offset: int = 0,
    limit: int = 20,
    sort: List[str] = ("+status", "+severity", "-queryname"),
) -> dict:
    return SastResultsAPI().get_sast_results_by_scan_id(
        scan_id=scan_id,
        severity=severity,
        state=state,
        status=status,
        query_group=query_group,
        compliance=compliance,
        query=query,
        language=language,
        query_ids=query_ids,
        node_ids=node_ids,
        source_file=source_file,
        source_file_operation=source_file_operation,
        source_node=source_node,
        source_node_operation=source_node_operation,
        source_line=source_line,
        source_line_operation=source_line_operation,
        sink_node=sink_node,
        sink_node_operation=sink_node_operation,
        sink_file=sink_file,
        sink_file_operation=sink_file_operation,
        sink_line=sink_line,
        sink_line_operation=sink_line_operation,
        number_of_nodes=number_of_nodes,
        number_of_nodes_operation=number_of_nodes_operation,
        notes=notes,
        notes_operation=notes_operation,
        first_found_at=first_found_at,
        first_found_at_operation=first_found_at_operation,
        preset_id=preset_id,
        result_id=result_id,
        category=category,
        search=search,
        include_nodes=include_nodes,
        apply_predicates=apply_predicates,
        offset=offset,
        limit=limit,
        sort=sort,
    )
