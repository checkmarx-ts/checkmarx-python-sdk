from .httpRequests import get_request
from .utilities import get_url_param, type_check, list_member_type_check
from .dto import KicsResult

api_url = "/api/kics-results"


def get_kics_results_by_scan_id(scan_id, severity=None, status=None, source_file=None, apply_predicates=True, offset=0,
                                limit=20, sort=None):
    """

    Args:
        scan_id (str): filter by scan id
        severity (list of str): filter by severity. OR operator between the items.
                            Available values : HIGH, MEDIUM, LOW, INFO
        status (list of str): filter by status. OR operator between the items.
                            Available values : NEW, RECURRENT, FIXED
        source_file (str): filter by source file name.
        apply_predicates (bool): if true will apply changes from predicates, otherwise will return the raw result.
                    Default value : true
        offset (int): The number of items to skip before starting to collect the result set.
                    Default value : 0
        limit (int): The number of items to return.
                    Default value : 20
        sort (list of str): sorting ORDERED array. each string pattern "[-+]field". - mean ASC, + mean DESC.
                    Available values : -severity, +severity, -status, +status, -firstfoundat, +firstfoundat, -foundat,
                        +foundat, firstscanid, +firstscanid
                    Default value : List [ "+status", "+severity" ]
    Returns:

    """

    type_check(scan_id, str)
    type_check(severity, (list, tuple))
    type_check(status, (list, tuple))
    type_check(source_file, str)
    type_check(apply_predicates, bool)
    type_check(sort, (list, tuple))

    list_member_type_check(severity, str)
    list_member_type_check(status, str)
    list_member_type_check(sort, str)

    relative_url = api_url + "?scan-id={scan_id}".format(scan_id=scan_id)
    relative_url += get_url_param("severity", severity)
    relative_url += get_url_param("status", status)
    relative_url += get_url_param("offset", offset)
    relative_url += get_url_param("limit", limit)
    relative_url += get_url_param("sort", sort)
    response = get_request(relative_url=relative_url)
    response = response.json()
    return {
        "results": [
            KicsResult(
                kics_result_id=result.get("ID"),
                similarity_id=result.get("similarityID"),
                severity=result.get("severity"),
                first_scan_id=result.get("firstScanID"),
                first_found_at=result.get("firstFoundAt"),
                found_at=result.get("foundAt"),
                status=result.get("status"),
                state=result.get("state"),
                kics_type=result.get("type"),
                query_id=result.get("queryID"),
                query_name=result.get("queryName"),
                query_group=result.get("group"),
                query_url=result.get("queryUrl"),
                file_name=result.get("fileName"),
                line=result.get("line"),
                platform=result.get("platform"),
                issue_type=result.get("issueType"),
                search_key=result.get("searchKey"),
                search_value=result.get("searchValue"),
                expected_value=result.get("expectedValue"),
                actual_value=result.get("actualValue"),
                value=result.get("value"),
                description=result.get("description"),
                comments=result.get("comments"),
                category=result.get("category"),
            ) for result in response.get("results") or []
        ],
        "totalCount": response.get("totalCount"),
    }
