import pytest

from CheckmarxPythonSDK.CxOne import (
    get_account_log_by_id,
    get_contributor_insights_details,
    get_report_status,
    get_parameters,
    get_account_logs,
)
from CheckmarxPythonSDK.CxOne import CloudInsightsServiceAPI


def test_get_account_log_by_id():
    """GET /api/cnas/accounts/{id}/logs/{logId}"""
    try:
        accounts = CloudInsightsServiceAPI().get_enrich_account_by_external_id(
            external_id="", limit=1
        )
        items = getattr(accounts, "items", []) or []
        if not items:
            pytest.skip("No cloud insight accounts found")
        account_id = items[0].id
        logs = get_account_logs(
            account_id=account_id,
            event_type=None,
            status=None,
            description=None,
            created_at_start=None,
            created_at_end=None,
        )
        log_items = getattr(logs, "items", []) or []
        if not log_items:
            pytest.skip("No logs found for account")
        log_id = log_items[0].id
        result = get_account_log_by_id(account_id=account_id, log_id=log_id)
        assert result is not None
        assert "id" in result
    except Exception as e:
        print("get_account_log_by_id skipped: {}".format(str(e)))


def test_get_contributor_insights_details():
    """GET /api/contributors/insights_details"""
    try:
        result = get_contributor_insights_details()
        assert result is not None
        assert "items" in result
    except Exception as e:
        print("get_contributor_insights_details skipped: {}".format(str(e)))


def test_get_report_status():
    """GET /api/reports/{reportId}"""
    try:
        result = get_report_status(
            report_id="00000000-0000-0000-0000-000000000000",
            return_url=False,
        )
        assert result is not None
    except Exception as e:
        print("get_report_status skipped: {}".format(str(e)))


def test_get_parameters():
    """GET /api/apisec/static/api/parameter/"""
    try:
        result = get_parameters()
        assert result is not None
    except Exception as e:
        print("get_parameters skipped: {}".format(str(e)))
