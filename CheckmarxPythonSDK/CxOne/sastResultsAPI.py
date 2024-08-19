from .httpRequests import get_request
from .utilities import get_url_param, type_check, list_member_type_check
from .dto import SastResult, ResultNode, construct_result_node, construct_sast_result, construct_sast_result

api_url = "/api/sast-results"


def get_sast_results_by_scan_id(scan_id, severity=None, state=None, status=None, query_group=None, compliance=None,
                                query=None,language=None, query_ids=None, node_ids=None, source_file=None,
                                source_file_operation=None, source_node=None, source_node_operation=None,
                                source_line=None, source_line_operation=None,
                                sink_node=None, sink_node_operation=None, sink_file=None, sink_file_operation=None,
                                sink_line=None, sink_line_operation=None,
                                number_of_nodes=None, number_of_nodes_operation=None, notes=None, notes_operation=None,
                                first_found_at=None, first_found_at_operation=None, preset_id=None, result_id=None,
                                category=None, search=None,
                                include_nodes=True, apply_predicates=True, offset=0, limit=20, sort=None):
    """

    Args:
        scan_id (str): filter by scan id
        severity (list of str): filter by severity. OR operator between the items.
                        Available values : CRITICAL, HIGH, MEDIUM, LOW, INFO
        state (list of str): TO_VERIFY, NOT_EXPLOITABLE, PROPOSED_NOT_EXPLOITABLE, CONFIRMED, URGENT
        status (list of str): filter by status. OR operator between the items.
                        Available values : NEW, RECURRENT, FIXED
        query_group (str): filter results by the vulnerability group. Note: Can be a substring of the group name.
        compliance (str): Filter by compliance standard. Note: Must be an exact match, case insensitive.
        query (str): Filter results by query. Note: Must be an exact match.
        language (list of str): Filter results by the language. Note: Must be an exact match, case insensitive.
        query_ids (list of str): filter by queries ids. Note: Must be an exact match.
        node_ids (list of str): Filter results by Node IDs. Note: OR operator for multiple IDs.
        source_file (str): filter by source file name.
        source_file_operation (str): filter operation for source file.
                        Available values : LESS_THAN, GREATER_THAN, CONTAINS, NOT_CONTAINS, EQUAL, NOT_EQUAL, START_WITH
        source_node (str): filter by source node
        source_node_operation (str): filter operation for source node
                        Available values : LESS_THAN, GREATER_THAN, CONTAINS, NOT_CONTAINS, EQUAL, NOT_EQUAL, START_WITH
        source_line (int): Filter results by source line.
        source_line_operation (str): The operator that you would like to apply to the specified source line value.
                        Available values : LESS_THAN, GREATER_THAN, EQUAL, NOT_EQUAL
        sink_node (str): filter by sink node
        sink_node_operation (str): filter operation for sink node
                        Available values : LESS_THAN, GREATER_THAN, CONTAINS, NOT_CONTAINS, EQUAL, NOT_EQUAL, START_WITH
        sink_file (str): filter by sink file name
        sink_file_operation (str): filter operation for sink file
                        Available values : LESS_THAN, GREATER_THAN, CONTAINS, NOT_CONTAINS, EQUAL, NOT_EQUAL, START_WITH
        sink_line (int): Filter results by sink line.
        sink_line_operation (str): The operator that you would like to apply to the specified sink line value.
        number_of_nodes (int): Filter results by number of nodes.
        number_of_nodes_operation (str): The operator that you would like to apply to the specified number of nodes value.
                        Available values : LESS_THAN, GREATER_THAN, EQUAL, NOT_EQUAL
        notes (str): Filter results by last notes.
        notes_operation (str): The operator that you would like to apply to the specified notes value.
                        Available values : CONTAINS, START_WITH
        first_found_at (str): Filter results by first found at.
        first_found_at_operation (str): The operator that you would like to apply to the specified first found at value.
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

    relative_url = api_url + "?scan-id={scan_id}".format(scan_id=scan_id)
    relative_url += get_url_param("severity", severity)
    relative_url += get_url_param("state", state)
    relative_url += get_url_param("status", status)
    relative_url += get_url_param("group", query_group)
    relative_url += get_url_param("compliance", compliance)
    relative_url += get_url_param("query", query)
    relative_url += get_url_param("language", language)
    relative_url += get_url_param("query-ids", query_ids)
    relative_url += get_url_param("node-ids", node_ids)
    relative_url += get_url_param("source-file", source_file)
    relative_url += get_url_param("source-file-operation", source_file_operation)
    relative_url += get_url_param("source-node", source_node)
    relative_url += get_url_param("source-node-operation", source_node_operation)
    relative_url += get_url_param("source-line", source_line)
    relative_url += get_url_param("source-line-operation", source_line_operation)
    relative_url += get_url_param("sink-node", sink_node)
    relative_url += get_url_param("sink-node-operation", sink_node_operation)
    relative_url += get_url_param("sink-file", sink_file)
    relative_url += get_url_param("sink-file-operation", sink_file_operation)
    relative_url += get_url_param("sink-line", sink_line)
    relative_url += get_url_param("sink-line-operation", sink_line_operation)
    relative_url += get_url_param("number-of-nodes", number_of_nodes)
    relative_url += get_url_param("number-of-nodes-operation", number_of_nodes_operation)
    relative_url += get_url_param("notes", notes)
    relative_url += get_url_param("notes-operation", notes_operation)
    relative_url += get_url_param("first-found-at", first_found_at)
    relative_url += get_url_param("first-found-at-operation", first_found_at_operation)
    relative_url += get_url_param("preset-id", preset_id)
    relative_url += get_url_param("result-id", result_id)
    relative_url += get_url_param("category", category)
    relative_url += get_url_param("search", search)
    relative_url += get_url_param("include-nodes", include_nodes)
    relative_url += get_url_param("apply-predicates", apply_predicates)
    relative_url += get_url_param("offset", offset)
    relative_url += get_url_param("limit", limit)
    relative_url += get_url_param("sort", sort)
    response = get_request(relative_url=relative_url)
    response = response.json()
    return {
        "results": [
            construct_sast_result(result) for result in response.get("results") or []
        ],
        "totalCount": response.get("totalCount")
    }
