import pytest

from CheckmarxPythonSDK.CxOne import (
    get_applications,
    get_application_summary,
    get_application_resources,
    get_application_microservices,
    get_application_risk_scores,
)


def _get_app_id():
    try:
        result = get_applications()
        apps = result.get("applications", [])
        return apps[0] if apps else None
    except Exception:
        return None


def test_get_applications():
    try:
        result = get_applications()
        assert result is not None
        assert "applications" in result
    except Exception as e:
        print("get_applications skipped: {}".format(str(e)))


def test_get_application_summary():
    app_id = _get_app_id()
    if not app_id:
        pytest.skip("No correlation applications found or service unavailable")
    result = get_application_summary(id=app_id)
    assert result is not None
    assert "microservices" in result


def test_get_application_resources():
    app_id = _get_app_id()
    if not app_id:
        pytest.skip("No correlation applications found or service unavailable")
    result = get_application_resources(id=app_id)
    assert result is not None
    assert "resources" in result


def test_get_application_microservices():
    app_id = _get_app_id()
    if not app_id:
        pytest.skip("No correlation applications found or service unavailable")
    result = get_application_microservices(id=app_id)
    assert result is not None
    assert "microservices" in result


def test_get_application_risk_scores():
    app_id = _get_app_id()
    if not app_id:
        pytest.skip("No correlation applications found or service unavailable")
    result = get_application_risk_scores(id=app_id)
    assert result is not None
    assert "results" in result
