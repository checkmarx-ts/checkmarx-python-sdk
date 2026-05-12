import pytest
from CheckmarxPythonSDK.CxOne import (
    get_sast_results_by_scan_id,
)
from CheckmarxPythonSDK.CxOne import ScansAPI as _ScansAPI


def _get_sast_scan_id():
    result = _ScansAPI().get_a_list_of_scans(limit=10, statuses=["Completed"])
    for scan in result.scans:
        if "sast" in (scan.engines or []):
            return scan.id
    return None


def test_get_sast_results_by_scan_id():
    scan_id = _get_sast_scan_id()
    if not scan_id:
        pytest.skip("No completed SAST scan found")
    offset = 0
    limit = 500
    page = 1
    sast_results_collection = get_sast_results_by_scan_id(scan_id=scan_id, offset=offset, limit=limit, state=["TO_VERIFY", "CONFIRMED"], include_nodes=False,)
    total_count = int(sast_results_collection.get("totalCount"))
    print(f"number of totalCount results: {total_count}")
    sast_results = sast_results_collection.get("results")
    if total_count > limit:
        while True:
            offset = page * limit
            if offset >= total_count:
                break
            sast_results_collection = get_sast_results_by_scan_id(scan_id=scan_id, offset=offset, limit=limit, state=["TO_VERIFY", "CONFIRMED"], include_nodes=False,)
            page += 1
            sast_results.extend(sast_results_collection.get("results"))
    print(f"number of TO_VERIFY or CONFIRMED results: {len(sast_results)}")
    pass
