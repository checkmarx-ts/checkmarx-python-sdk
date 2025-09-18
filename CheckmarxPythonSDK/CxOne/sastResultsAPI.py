from CheckmarxPythonSDK.api_client import ApiClient
from CheckmarxPythonSDK.CxOne.config import construct_configuration
from typing import List
from .utilities import type_check, list_member_type_check
from .dto import construct_sast_result

api_url = "/api/sast-results"


class SastResultsAPI(object):

    def __init__(self, api_client: ApiClient = None):
        if api_client is None:
            configuration = construct_configuration()
            api_client = ApiClient(configuration=configuration)
        self.api_client = api_client

    def get_sast_results_by_scan_id(
            self, scan_id: str, severity: List[str] = None, state: List[str] = None, status: List[str] = None,
            query_group: str = None, compliance: str = None, query: str = None, language: List[str] = None,
            query_ids: List[str] = None, node_ids: List[str] = None, source_file: str = None,
            source_file_operation: str = None, source_node: str = None, source_node_operation: str = None,
            source_line: int = None, source_line_operation: str = None,
            sink_node: str = None, sink_node_operation: str = None,
            sink_file: str = None, sink_file_operation: str = None,
            sink_line: int = None, sink_line_operation: str = None,
            number_of_nodes: int = None, number_of_nodes_operation: str = None,
            notes: str = None, notes_operation: str = None,
            first_found_at: str = None, first_found_at_operation: str = None,
            preset_id: str = None, result_id: List[str] = None, category: str = None, search: str = None,
            include_nodes: bool = True, apply_predicates: bool = True, offset: int = 0, limit: int = 20,
            sort: List[str] = ("+status", "+severity", "-queryname")
    ) -> dict:
        """

        Args:
            scan_id (str): filter by scan id
            severity (list of str): filter by severity. OR operator between the items.
                            Available values : CRITICAL, HIGH, MEDIUM, LOW, INFO
            state (list of str): TO_VERIFY, NOT_EXPLOITABLE, PROPOSED_NOT_EXPLOITABLE, CONFIRMED, URGENT
            status (list of str): filter by status. OR operator between the items.
                            Available values : NEW, RECURRENT, FIXED
            query_group (str): filter results by the vulnerability group. Note: Can be a substring of the group name.
            compliance (str): Filter by compliance standard. Note: Must be an exact match, case-insensitive.
            query (str): Filter results by query. Note: Must be an exact match.
            language (list of str): Filter results by the language. Note: Must be an exact match, case-insensitive.
            query_ids (list of str): filter by queries ids. Note: Must be an exact match.
            node_ids (list of str): Filter results by Node IDs. Note: OR operator for multiple IDs.
            source_file (str): filter by source file name.
            source_file_operation (str): filter operation for source file.
                            Available values : LESS_THAN, GREATER_THAN, CONTAINS, NOT_CONTAINS, EQUAL, NOT_EQUAL,
                            START_WITH
            source_node (str): filter by source node
            source_node_operation (str): filter operation for source node
                            Available values : LESS_THAN, GREATER_THAN, CONTAINS, NOT_CONTAINS, EQUAL, NOT_EQUAL,
                            START_WITH
            source_line (int): Filter results by source line.
            source_line_operation (str): The operator that you would like to apply to the specified source line value.
                            Available values : LESS_THAN, GREATER_THAN, EQUAL, NOT_EQUAL
            sink_node (str): filter by sink node
            sink_node_operation (str): filter operation for sink node
                            Available values : LESS_THAN, GREATER_THAN, CONTAINS, NOT_CONTAINS, EQUAL, NOT_EQUAL,
                            START_WITH
            sink_file (str): filter by sink file name
            sink_file_operation (str): filter operation for sink file
                            Available values : LESS_THAN, GREATER_THAN, CONTAINS, NOT_CONTAINS, EQUAL, NOT_EQUAL,
                            START_WITH
            sink_line (int): Filter results by sink line.
            sink_line_operation (str): The operator that you would like to apply to the specified sink line value.
            number_of_nodes (int): Filter results by number of nodes.
            number_of_nodes_operation (str): The operator that you would like to apply to the specified number of nodes
                            value.
                            Available values : LESS_THAN, GREATER_THAN, EQUAL, NOT_EQUAL
            notes (str): Filter results by last notes.
            notes_operation (str): The operator that you would like to apply to the specified notes value.
                            Available values : CONTAINS, START_WITH
            first_found_at (str): Filter results by first found at.
            first_found_at_operation (str): The operator that you would like to apply to the specified first found at
                        value.
                        (defaults to GREATER_THAN)
                        Available values : LESS_THAN, GREATER_THAN
            preset_id (str): Filter results by preset
            result_id (list of str): filter by unique result hash
            category (str): Filter results by category name.
            search (str): Filter results by source file name, source node, sink node, sink file name, notes.
            include_nodes (bool): if true returns ResultNode objects, otherwise will omit the Nodes field.
                            Default value : true
            apply_predicates (bool): if true will apply changes from predicates, otherwise will return the raw result.
                            Default value : true
            offset (int): The number of items to skip before starting to collect the result set.
                            Default value : 0
            limit (int): The number of items to return.
                            Default value : 20
            sort (list of str): sorting ORDERED array. each string pattern "[-+]field". - mean ASC, + mean DESC.
                            Available values : -severity, +severity, -status, +status, -firstfoundat, +firstfoundat,
                            -foundat, +foundat, -queryname, +queryname, -firstscanid, +firstscanid
                            Default value : List [ "+status", "+severity", "-queryname" ]

        Returns:
            dict
        """

        type_check(scan_id, str)
        type_check(severity, (list, tuple))
        type_check(state, (list, tuple))
        type_check(status, (list, tuple))
        type_check(query_group, str)
        type_check(compliance, str)
        type_check(query, str)
        type_check(language, (list, tuple))
        type_check(query_ids, (list, tuple))
        type_check(node_ids, (list, tuple))
        type_check(source_file, str)
        type_check(source_file_operation, str)
        type_check(source_node, str)
        type_check(source_node_operation, str)
        type_check(source_line, int)
        type_check(source_line_operation, str)
        type_check(sink_node, str)
        type_check(sink_node_operation, str)
        type_check(sink_file, str)
        type_check(sink_file_operation, str)
        type_check(sink_line, int)
        type_check(sink_line_operation, str)
        type_check(number_of_nodes, int)
        type_check(number_of_nodes_operation, str)
        type_check(notes, str)
        type_check(notes_operation, str)
        type_check(first_found_at, str)
        type_check(first_found_at_operation, str)
        type_check(preset_id, str)
        type_check(result_id, (list, tuple))
        type_check(category, str)
        type_check(search, str)
        type_check(include_nodes, bool)
        type_check(apply_predicates, bool)
        type_check(offset, int)
        type_check(limit, int)
        type_check(sort, (list, tuple))
        list_member_type_check(severity, str)
        list_member_type_check(status, str)
        list_member_type_check(language, str)
        list_member_type_check(query_ids, str)
        list_member_type_check(node_ids, str)
        list_member_type_check(sort, str)
        relative_url = api_url
        params = {
            "scan-id": scan_id, "severity": severity, "state": state, "status": status, "group": query_group,
            "compliance": compliance, "query": query, "language": language, "query-ids": query_ids,
            "node-ids": node_ids,
            "source-file": source_file, "source-file-operation": source_file_operation,
            "source-node": source_node, "source-node-operation": source_node_operation,
            "source-line": source_line, "source-line-operation": source_line_operation,
            "sink-node": sink_node, "sink-node-operation": sink_node_operation,
            "sink-file": sink_file, "sink-file-operation": sink_file_operation,
            "sink-line": sink_line, "sink-line-operation": sink_line_operation,
            "number-of-nodes": number_of_nodes, "number-of-nodes-operation": number_of_nodes_operation,
            "notes": notes, "notes-operation": notes_operation,
            "first-found-at": first_found_at, "first-found-at-operation": first_found_at_operation,
            "preset-id": preset_id, "result-id": result_id, "category": category, "search": search,
            "include-nodes": include_nodes, "apply-predicates": apply_predicates,
            "offset": offset, "limit": limit, "sort": ",".join(sort) if sort else None
        }
        response = self.api_client.get_request(relative_url=relative_url, params=params)
        response = response.json()
        return {
            "results": [
                construct_sast_result(result) for result in response.get("results") or []
            ],
            "totalCount": response.get("totalCount")
        }


def get_sast_results_by_scan_id(
            scan_id: str, severity: List[str] = None, state: List[str] = None, status: List[str] = None,
            query_group: str = None, compliance: str = None, query: str = None, language: List[str] = None,
            query_ids: List[str] = None, node_ids: List[str] = None, source_file: str = None,
            source_file_operation: str = None, source_node: str = None, source_node_operation: str = None,
            source_line: int = None, source_line_operation: str = None,
            sink_node: str = None, sink_node_operation: str = None,
            sink_file: str = None, sink_file_operation: str = None,
            sink_line: int = None, sink_line_operation: str = None,
            number_of_nodes: int = None, number_of_nodes_operation: str = None,
            notes: str = None, notes_operation: str = None,
            first_found_at: str = None, first_found_at_operation: str = None,
            preset_id: str = None, result_id: List[str] = None, category: str = None, search: str = None,
            include_nodes: bool = True, apply_predicates: bool = True, offset: int = 0, limit: int = 20,
            sort: List[str] = ("+status", "+severity", "-queryname")
) -> dict:
    return SastResultsAPI().get_sast_results_by_scan_id(
        scan_id=scan_id, severity=severity, state=state, status=status, query_group=query_group, compliance=compliance,
        query=query, language=language, query_ids=query_ids, node_ids=node_ids,
        source_file=source_file, source_file_operation=source_file_operation,
        source_node=source_node, source_node_operation=source_node_operation,
        source_line=source_line, source_line_operation=source_line_operation,
        sink_node=sink_node, sink_node_operation=sink_node_operation,
        sink_file=sink_file, sink_file_operation=sink_file_operation,
        sink_line=sink_line, sink_line_operation=sink_line_operation,
        number_of_nodes=number_of_nodes, number_of_nodes_operation=number_of_nodes_operation,
        notes=notes, notes_operation=notes_operation,
        first_found_at=first_found_at, first_found_at_operation=first_found_at_operation,
        preset_id=preset_id, result_id=result_id, category=category, search=search,
        include_nodes=include_nodes, apply_predicates=apply_predicates,
        offset=offset, limit=limit, sort=sort,
    )
