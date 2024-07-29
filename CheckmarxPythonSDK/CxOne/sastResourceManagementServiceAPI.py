from .httpRequests import get_request, delete_request
from .utilities import get_url_param, type_check, list_member_type_check
from .dto import SastScan, Property
from CheckmarxPythonSDK.utilities.compat import OK, NO_CONTENT

api_url = "/api/sast-rm"


def construct_sast_scan(item):
    return SastScan(
        scan_id=item.get("id"),
        state=item.get("state"),
        queue_at=item.get("queuedAt"),
        allocated_at=item.get("allocatedAt"),
        running_at=item.get("runningAt"),
        engine=item.get("engine"),
        properties=[
            Property(
                key=prop.get("key"),
                value=prop.get("value"),
            ) for prop in item.get("properties")
        ]
    )


def get_sast_scan_allocation_info(scan_id):
    """

    Args:
        scan_id (str):

    Returns:

    """
    relative_url = api_url + "/scans/{id}".format(id=scan_id)
    response = get_request(relative_url=relative_url)
    item = response.json()
    return construct_sast_scan(item)


def delete_sast_scan(scan_id):
    """

    Args:
        scan_id (str):

    Returns:

    """
    is_successful = False
    relative_url = api_url + "/scans/{id}".format(id=scan_id)
    response = delete_request(relative_url=relative_url)
    if response.status_code == NO_CONTENT:
        is_successful = True
    return is_successful


def get_sast_scans(offset=0, limit=20, ids=None, with_deleted=None):
    """

    Args:
        offset (int): The number of items to skip before starting to collect the result set.
        limit (int): The number of items to return.
        ids (list of str): Ids of scans to return.
        with_deleted (bool): If deleted scans should be included in result.

    Returns:

    """
    type_check(offset, int)
    type_check(limit, int)
    type_check(ids, list)
    list_member_type_check(ids, str)
    type_check(with_deleted, bool)

    relative_url = api_url + "/scans?offset={}&limit={}".format(
        offset, limit
    )
    relative_url += get_url_param("ids", ids)
    relative_url += get_url_param("with-deleted", with_deleted)
    response = get_request(relative_url=relative_url)
    item = response.json()
    return {
        "totalCount": 0,
        "scans": [
            construct_sast_scan(scan) for scan in item.get("scans")
        ]
    }
