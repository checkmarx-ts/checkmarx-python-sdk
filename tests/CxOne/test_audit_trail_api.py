from CheckmarxPythonSDK.CxOne import (
    get_audit_events_for_tenant
)


def test_get_audit_events_for_tenant():
    result = get_audit_events_for_tenant(limit=1000)
    assert result is not None
