from CheckmarxPythonSDK.CxOne import get_audit_events


def test_get_audit_events():
    result = get_audit_events(limit=5)
    assert result is not None
    assert "events" in result
