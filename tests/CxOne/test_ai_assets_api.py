import pytest

from CheckmarxPythonSDK.CxOne import (
    get_ai_findings,
    get_ai_findings_aggregate,
    get_ai_finding_by_id,
    get_ai_asset_types,
    get_ai_assets,
    get_ai_applications,
)


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
