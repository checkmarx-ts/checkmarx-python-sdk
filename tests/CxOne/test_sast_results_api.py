from CheckmarxPythonSDK.CxOne import (
    get_sast_results_by_scan_id,
)


def test_get_sast_results_by_scan_id():
    # scan_id = "efc2911b-3ee0-4aa3-bc79-90fe97bc8103"
    scan_id = "d8aee11e-6ff1-40bc-9dd0-f855b050af59"
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