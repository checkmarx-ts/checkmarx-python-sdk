from .httpRequests import get_request
from .utilities import get_url_param, type_check, list_member_type_check
from .dto import (
    ResultsSummary,
    KicsCounters,
    SastCounters,
    ScaCounters,
    ScaPackageCounters,
    ScaContainersCounters,
    ApiSecCounters,
)

api_url = "/api/scan-summary"


def get_summary_for_many_scans(scan_ids, include_severity_status=True, include_queries=False, include_files=False,
                               apply_predicates=True, language=None):
    """

    Args:
        scan_ids (list of str): Scan IDs to find. Each scan id will have his own object.
        include_severity_status (bool): if true returns the severityStatus field, otherwise will omit the field.
                            Default value : true
        include_queries (bool): if true returns the queries field, otherwise will omit the field.
                            Default value : false
        include_files (bool): if true returns the source code file and sink code file fields, otherwise will omit the fields.
                            Default value : false
        apply_predicates (bool): if true will apply changes from predicates, otherwise will return the raw results summary.
                            Default value : true
        language (str): get scan summary for specific source code language.

    Returns:
        dict
    """
    type_check(scan_ids, (list, tuple))
    type_check(include_severity_status, bool)
    type_check(include_queries, bool)
    type_check(include_files, bool)
    type_check(apply_predicates, bool)
    type_check(language, str)

    list_member_type_check(scan_ids, str)

    relative_url = api_url + "?"
    relative_url += get_url_param("scan-ids", scan_ids)
    relative_url += get_url_param("include-severity-status", include_severity_status)
    relative_url += get_url_param("include-queries", include_queries)
    relative_url += get_url_param("include-files", include_files)
    relative_url += get_url_param("apply-predicates", apply_predicates)
    relative_url += get_url_param("language", language)

    response = get_request(relative_url=relative_url)
    response = response.json()
    return {
        "scansSummaries": [
            ResultsSummary(
                scan_id=summary.get("scanId"),
                sast_counters=summary.get("sastCounters"),
                kics_counters=summary.get("kicsCounters"),
                sca_counters=summary.get("scaCounters"),
                sca_packages_counters=summary.get('scaPackagesCounters'),
                sca_containers_counters=summary.get('scaContainersCounters'),
                api_sec_counters=summary.get('apiSecCounters')
            ) for summary in response.get("scansSummaries") or []
        ],
        "totalCount": response.get("totalCount")
    }


def get_sast_aggregate_results(scan_id, group_by_field, language=None, status=None, severity=None, source_file=None,
                               source_file_operation=None, source_node=None, source_node_operation=None,
                               sink_node=None, sink_node_operation=None, sink_file=None, sink_file_operation=None,
                               query_ids=None, apply_predicates=None, limit=20, offset=0):
    """

    Args:
        scan_id (str): filter by scan id
        group_by_field (list of str): fields to group results
                Available values : QUERY, SEVERITY, STATUS, SOURCE_NODE, SINK_NODE, SOURCE_FILE, SINK_FILE, LANGUAGE
        language (list of str): filter by language name. matching languages that EQUALS the input with case insensitive.
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

    relative_url = api_url + "?scan-id={scan_id}"
    relative_url += get_url_param("group-by-field", group_by_field)
    relative_url += get_url_param("language", language)
    relative_url += get_url_param("status", status)
    relative_url += get_url_param("severity", severity)
    relative_url += get_url_param("source-file", source_file)
    relative_url += get_url_param("source-file-operation", sink_file_operation)
    relative_url += get_url_param("source-node", source_node)
    relative_url += get_url_param("source-node-operation", source_node_operation)
    relative_url += get_url_param("sink-node", sink_node)
    relative_url += get_url_param("sink-node-operation", sink_node_operation)
    relative_url += get_url_param("sink-file", sink_file)
    relative_url += get_url_param("sink-file-operation", sink_file_operation)
    relative_url += get_url_param("query-ids", query_ids)
    relative_url += get_url_param("apply-predicates", apply_predicates)
    relative_url += get_url_param("limit", limit)
    relative_url += get_url_param("offset", offset)
    response = get_request(relative_url=relative_url)
    response = response.json()
    return response
