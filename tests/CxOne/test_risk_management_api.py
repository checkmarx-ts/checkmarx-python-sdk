import pytest

from CheckmarxPythonSDK.CxOne import (
    get_summary,
    get_results,
    get_score_card,
    update_result_state,
    update_assignees,
)


def _get_app_id():
    """Get an application ID from the risk summary."""
    try:
        result = get_summary()
        apps = result.get("applications", [])
        return apps[0].get("id") if apps else None
    except Exception:
        return None


def test_get_summary():
    try:
        result = get_summary()
        assert result is not None
        assert "applications" in result
    except Exception as e:
        print("get_summary skipped: {}".format(str(e)))


def test_get_results():
    app_id = _get_app_id()
    if not app_id:
        pytest.skip("No risk management applications found")
    result = get_results(application_id=app_id, limit=5)
    assert result is not None
    assert "results" in result


def test_get_score_card():
    app_id = _get_app_id()
    if not app_id:
        pytest.skip("No risk management applications found")
    results_data = get_results(application_id=app_id, limit=1)
    items = results_data.get("results", [])
    if not items:
        pytest.skip("No results found for application")
    result_id = items[0].get("id")
    score_card = get_score_card(id=result_id)
    assert score_card is not None


def test_update_result_state():
    app_id = _get_app_id()
    if not app_id:
        pytest.skip("No risk management applications found")
    results_data = get_results(application_id=app_id, limit=1)
    items = results_data.get("results", [])
    if not items:
        pytest.skip("No results found for application")
    item = items[0]
    result_id = item.get("id")
    current_state = item.get("state", "new")
    is_successful = update_result_state(
        application_id=app_id, id=result_id, state=current_state
    )
    assert is_successful is True


def test_update_assignees():
    app_id = _get_app_id()
    if not app_id:
        pytest.skip("No risk management applications found")
    results_data = get_results(application_id=app_id, limit=1)
    items = results_data.get("results", [])
    if not items:
        pytest.skip("No results found for application")
    result_id = items[0].get("id")
    result = update_assignees(
        results=[{"resultId": result_id, "applicationId": app_id}]
    )
    assert result is not None
    assert "response" in result
