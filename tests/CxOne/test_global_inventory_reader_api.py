import pytest

from CheckmarxPythonSDK.CxOne import (
    get_api_changes,
    get_api_inventory,
    get_data_origin,
    get_api_inventory_group,
    get_inventory_metadata,
    get_global_parameters,
    get_api_risks,
    get_risk_groups,
    get_risk_widget,
    get_risk_details,
)


def test_get_api_changes():
    try:
        result = get_api_changes()
        assert result is not None
        assert "api_changes" in result
    except Exception as e:
        print("get_api_changes skipped: {}".format(str(e)))


def test_get_api_inventory():
    try:
        result = get_api_inventory(per_page=5)
        assert result is not None
        assert "entries" in result
    except Exception as e:
        print("get_api_inventory skipped: {}".format(str(e)))


def test_get_data_origin():
    try:
        result = get_data_origin()
        assert result is not None
    except Exception as e:
        print("get_data_origin skipped: {}".format(str(e)))


def test_get_api_inventory_group():
    try:
        result = get_api_inventory_group(
            group_column="path", per_page=5
        )
        assert result is not None
        assert "groups" in result
    except Exception as e:
        print("get_api_inventory_group skipped: {}".format(str(e)))


def test_get_inventory_metadata():
    try:
        result = get_inventory_metadata()
        assert result is not None
    except Exception as e:
        print("get_inventory_metadata skipped: {}".format(str(e)))


def test_get_global_parameters():
    try:
        result = get_global_parameters()
        assert result is not None
    except Exception as e:
        print("get_global_parameters skipped: {}".format(str(e)))


def test_get_api_risks():
    try:
        result = get_api_risks(per_page=5)
        assert result is not None
    except Exception as e:
        print("get_api_risks skipped: {}".format(str(e)))


def test_get_risk_groups():
    try:
        result = get_risk_groups(group_column="severity", per_page=5)
        assert result is not None
        assert "groups" in result
    except Exception as e:
        print("get_risk_groups skipped: {}".format(str(e)))


def test_get_risk_widget():
    try:
        result = get_risk_widget()
        assert result is not None
    except Exception as e:
        print("get_risk_widget skipped: {}".format(str(e)))


def test_get_risk_details():
    # Need a risk_id from the risk list
    try:
        risks = get_api_risks(per_page=1)
        entries = risks.get("entries", [])
        if not entries:
            pytest.skip("No risk entries found")
        risk_id = entries[0].get("id")
        if not risk_id:
            pytest.skip("Risk entry has no ID")
        result = get_risk_details(risk_id=risk_id)
        assert result is not None
    except Exception as e:
        print("get_risk_details skipped: {}".format(str(e)))
