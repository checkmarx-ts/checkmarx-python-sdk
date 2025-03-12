from CheckmarxPythonSDK.CxOne import (
    get_sast_results_by_scan_id,
)


def test_get_sast_results_by_scan_id():
    scan_id = "efc2911b-3ee0-4aa3-bc79-90fe97bc8103"
    offset = 0
    limit = 100
    page = 1
    sast_results_collection = get_sast_results_by_scan_id(scan_id=scan_id, offset=offset, limit=limit)
    total_count = int(sast_results_collection.get("totalCount"))
    sast_results = sast_results_collection.get("results")
    if total_count > limit:
        while True:
            offset = page * limit
            if offset >= total_count:
                break
            sast_results_collection = get_sast_results_by_scan_id(scan_id=scan_id, offset=offset, limit=limit)
            page += 1
            sast_results.extend(sast_results_collection.get("results"))
    pass