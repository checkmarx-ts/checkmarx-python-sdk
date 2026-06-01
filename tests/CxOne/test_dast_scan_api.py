from CheckmarxPythonSDK.CxOne import get_tenant_overview, get_environments
from CheckmarxPythonSDK.CxOne.dto import (
    TenantOverview, DastEnvironmentsCollection, DastEnvironment,
)


def test_get_tenant_overview():
    overview = get_tenant_overview()
    assert isinstance(overview, TenantOverview)
    assert overview.tenant_id is not None
    assert overview.environments_count is not None
    assert overview.risk_rating is not None


def test_get_environments():
    collection = get_environments(to=5)
    assert isinstance(collection, DastEnvironmentsCollection)
    assert collection.total_items is not None
    assert isinstance(collection.environments, list)
    if collection.environments:
        env = collection.environments[0]
        assert isinstance(env, DastEnvironment)
        assert env.environment_id is not None
