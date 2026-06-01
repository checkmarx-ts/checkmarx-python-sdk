from CheckmarxPythonSDK.CxOne import get_tenant_overview
from CheckmarxPythonSDK.CxOne.dto import TenantOverview


def test_get_tenant_overview():
    overview = get_tenant_overview()
    assert isinstance(overview, TenantOverview)
    assert overview.tenant_id is not None
    assert overview.environments_count is not None
    assert overview.risk_rating is not None
