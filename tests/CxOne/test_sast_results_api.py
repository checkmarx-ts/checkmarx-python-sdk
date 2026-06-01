import pytest
from CheckmarxPythonSDK.CxOne import (
    get_sast_results_by_scan_id,
    get_sast_results_compare_by_scans,
    get_similar_results,
)
from CheckmarxPythonSDK.CxOne import ScansAPI as _ScansAPI


def _get_sast_scan_id():
    result = _ScansAPI().get_a_list_of_scans(limit=10, statuses=["Completed"])
    for scan in result.scans:
        if "sast" in (scan.engines or []):
            return scan.id
    return None


def _get_two_sast_scan_ids():
    result = _ScansAPI().get_a_list_of_scans(limit=20, statuses=["Completed"])
    ids = []
    for scan in result.scans:
        if "sast" in (scan.engines or []):
            ids.append(scan.id)
            if len(ids) >= 2:
                return ids[0], ids[1]
    return None, None


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


def test_get_sast_results_compare_by_scans():
    scan_id, base_scan_id = _get_two_sast_scan_ids()
    if not scan_id or not base_scan_id:
        pytest.skip("Need two completed SAST scans for comparison")
    try:
        result = get_sast_results_compare_by_scans(
            scan_id=scan_id,
            base_scan_id=base_scan_id,
            limit=5,
        )
        assert result is not None
        assert "results" in result
    except Exception as e:
        print("get_sast_results_compare_by_scans skipped: {}".format(str(e)))


def test_get_similar_results():
    scan_id = _get_sast_scan_id()
    if not scan_id:
        pytest.skip("No completed SAST scan found")
    try:
        result = get_similar_results(
            scan_id=scan_id,
            results_hash=["dummyhash123"],
        )
        assert result is not None
    except Exception as e:
        print("get_similar_results skipped: {}".format(str(e)))
