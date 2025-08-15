from CheckmarxPythonSDK.CxOne import (
    get_audit_events_for_tenant
)


def test_get_audit_events_for_tenant():
    result = get_audit_events_for_tenant(limit=1024)
    assert result is not None
    result = get_audit_events_for_tenant(date_from='2025-04-22', date_to='2025-08-15', limit=1024)
    assert result is not None
