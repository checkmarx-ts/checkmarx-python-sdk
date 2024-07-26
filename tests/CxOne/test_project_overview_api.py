from CheckmarxPythonSDK.CxOne import (
    get_tenant_projects_overview
)


def test_get_tenant_projects_overview():
    result = get_tenant_projects_overview()
    assert result is not None
