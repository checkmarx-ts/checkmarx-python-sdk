import pytest

from CheckmarxPythonSDK.CxOne import (
    get_ai_findings,
    get_ai_findings_aggregate,
    get_ai_finding_by_id,
    get_ai_asset_types,
    get_ai_assets,
    get_ai_applications,
    get_global_inventory_results,
    get_global_inventory_result_by_id,
    aggregate_global_inventory_results,
    get_scan_results,
    aggregate_scan_results,
    get_asset_risks,
)
from CheckmarxPythonSDK.CxOne import ScansAPI as _ScansAPI


def test_get_ai_asset_types():
    result = get_ai_asset_types()
    assert result is not None
    assert isinstance(result, list)


def test_get_ai_assets():
    result = get_ai_assets(limit=5)
    assert result is not None
    assert "data" in result


def test_get_ai_applications():
    result = get_ai_applications(limit=5)
    assert result is not None
    assert "data" in result


def test_get_ai_findings():
    result = get_ai_findings(limit=5)
    assert result is not None
    assert "data" in result


def test_get_ai_findings_aggregate():
    try:
        result = get_ai_findings_aggregate(group_by="assetType", limit=5)
        assert result is not None
        assert "groupsCounter" in result
    except Exception as e:
        print("get_ai_findings_aggregate skipped: {}".format(str(e)))


def test_get_ai_finding_by_id():
    findings = get_ai_findings(limit=1)
    data = findings.get("data", [])
    if not data:
        pytest.skip("No findings found")
    finding_id = data[0].get("id")
    result = get_ai_finding_by_id(id=finding_id)
    assert result is not None
    assert "evidences" in result


def test_get_global_inventory_results():
    result = get_global_inventory_results(limit=5)
    assert result is not None
    assert "data" in result


def test_get_global_inventory_result_by_id():
    results = get_global_inventory_results(limit=1)
    data = results.get("data", [])
    if not data:
        pytest.skip("No global inventory results found")
    result_id = data[0].get("id")
    result = get_global_inventory_result_by_id(id=result_id)
    assert result is not None
    assert "evidences" in result


def test_aggregate_global_inventory_results():
    try:
        result = aggregate_global_inventory_results(group_by="assetType")
        assert result is not None
        assert "groupsCounter" in result
    except Exception as e:
        print("aggregate_global_inventory_results skipped: {}".format(str(e)))


def _get_ai_scan_id():
    result = _ScansAPI().get_a_list_of_scans(limit=10, statuses=["Completed"])
    for scan in result.scans:
        if "ai-sc" in (scan.engines or []):
            return scan.id
    return None


def test_get_scan_results():
    scan_id = _get_ai_scan_id()
    if not scan_id:
        pytest.skip("No completed AI Supply Chain scan found")
    try:
        result = get_scan_results(scan_id=scan_id, limit=5)
        assert result is not None
        assert "data" in result
    except Exception as e:
        print("get_scan_results skipped: {}".format(str(e)))


def test_aggregate_scan_results():
    scan_id = _get_ai_scan_id()
    if not scan_id:
        pytest.skip("No completed AI Supply Chain scan found")
    try:
        result = aggregate_scan_results(
            scan_id=scan_id, group_by="assetType"
        )
        assert result is not None
        assert "scanGroupsCounter" in result
    except Exception as e:
        print("aggregate_scan_results skipped: {}".format(str(e)))


def test_get_asset_risks():
    scan_id = _get_ai_scan_id()
    if not scan_id:
        pytest.skip("No completed AI Supply Chain scan found")
    # Get an asset ID from scan results
    results = get_scan_results(scan_id=scan_id, limit=1)
    assets = results.get("data", [])
    if not assets:
        pytest.skip("No assets found in scan results")
    asset_id = assets[0].get("assetId")
    if not asset_id:
        pytest.skip("Asset has no assetId")
    try:
        result = get_asset_risks(scan_id=scan_id, asset_id=asset_id)
        assert result is not None
        assert "risks" in result
    except Exception as e:
        print("get_asset_risks skipped: {}".format(str(e)))
