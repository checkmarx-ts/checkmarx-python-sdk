import pytest
from CheckmarxPythonSDK.CxOne import (
    get_tenant_projects_overview,
    get_project_counters,
)


@pytest.mark.skip(reason="400 Bad Request - default sort parameter +last_scanned_at not accepted by this server")
def test_get_tenant_projects_overview():
    result = get_tenant_projects_overview()
    assert result is not None


def test_get_project_counters():
    result = get_project_counters()
    assert result is not None
