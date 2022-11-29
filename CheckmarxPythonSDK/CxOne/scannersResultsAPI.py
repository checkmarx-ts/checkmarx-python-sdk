from .httpRequests import get_request
from .utilities import get_url_param, type_check, list_member_type_check
from .dto import Result

api_url = "/api/results"


def get_all_scanners_results_by_scan_id(scan_id, severity=None, state=None, status=None, offset=0, limit=20, sort=None):
    """

    Args:
        scan_id (str): filter by scan id
        severity (list of str): filter by severity. OR operator between the items
                                Available values : HIGH, MEDIUM, LOW, INFO
        state (list of str): filter by state. OR operator between the items.
                        Available values : TO_VERIFY, NOT_EXPLOITABLE, PROPOSED_NOT_EXPLOITABLE, CONFIRMED, URGENT
        status (list of str): filter by status. OR operator between the items.
                        Available values : NEW, RECURRENT, FIXED
        offset (int): The number of items to skip before starting to collect the result set.
                        Default value : 0
        limit (int): The number of items to return.
                        Default value : 20
        sort (list of str): sorting ORDERED array. each string pattern "[-+]field". - mean ASC, + mean DESC.
                        Available values : -severity, +severity, -status, +status, -state, +state, -type, +type,
                                    -firstfoundat, +firstfoundat, -foundat, +foundat, -firstscanid, +firstscanid
                        Default value : List [ "+status", "+severity" ]

    Returns:
        dict
    """
    type_check(scan_id, str)
    type_check(severity, (list, tuple))
    type_check(state, (list, tuple))
    type_check(status, (list, tuple))
    type_check(offset, int)
    type_check(limit, int)
    type_check(sort, (list, tuple))

    list_member_type_check(severity, str)
    list_member_type_check(state, str)
    list_member_type_check(status, str)
    list_member_type_check(sort, str)

    relative_url = api_url + "?scan-id={scan_id}".format(scan_id=scan_id)
    relative_url += get_url_param("severity", severity)
    relative_url += get_url_param("state", state)
    relative_url += get_url_param("status", status)
    relative_url += get_url_param("offset", offset)
    relative_url += get_url_param("limit", limit)
    relative_url += get_url_param("sort", sort)
    response = get_request(relative_url=relative_url)
    response = response.json()
    return {
        "results": [
            Result(
                result_type=result.get("type"),
                result_id=result.get("id"),
                similarity_id=result.get('similarityId'),
                status=result.get("status"),
                state=result.get("state"),
                severity=result.get("severity"),
                confidence_level=result.get("confidenceLevel"),
                created=result.get("created"),
                first_found_at=result.get("firstFoundAt"),
                found_at=result.get("foundAt"),
                update_at=result.get("updateAt"),
                first_scan_id=result.get('firstScanId'),
                description=result.get("description"),
                data=result.get("data"),
                comments=result.get("comments"),
                vulnerability_details=result.get('vulnerabilityDetails'),
            ) for result in response.get("results") or []
        ],
        "totalCount": response.get("totalCount"),
    }
