from CheckmarxPythonSDK.CxOne import get_tenant_overview, get_environments
from CheckmarxPythonSDK.CxOne.dto import (
    TenantOverview, DastEnvironmentsCollection, DastEnvironment,
    DastEnvironmentFilter, DastLastRiskRating, DastAuthSuccess, DastTunnelState,
    DastSortBy, DastAlertRiskLevel, DastApplication, DastScanConfig,
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
        # Nested DTO typing
        assert env.scan_config is None or isinstance(env.scan_config, DastScanConfig)
        assert isinstance(env.applications, list)
        assert all(isinstance(a, DastApplication) for a in env.applications)
        assert env.alert_risk_level is None or isinstance(env.alert_risk_level, DastAlertRiskLevel)


def test_dast_environment_filter_to_dict():
    f = DastEnvironmentFilter(
        domain="example.com",
        last_risk_rating=DastLastRiskRating.HIGH,
        auth_success=DastAuthSuccess.NO_AUTH,
        tunnel_state=DastTunnelState.CONNECTED,
    )
    assert f.to_dict() == {
        "domain": "example.com",
        "lastRiskRating": "High",
        "authSuccess": "no_auth",
        "tunnelState": "connected",
    }


def test_get_environments_with_filter_dto():
    f = DastEnvironmentFilter(scan_type="DAST")
    collection = get_environments(filter=f, to=5)
    assert isinstance(collection, DastEnvironmentsCollection)
    for env in collection.environments:
        assert env.scan_type == "DAST" or "DAST" in (env.scan_type or "")


def test_dast_sort_by_enum_values():
    assert DastSortBy.CREATED.value == "created"
    assert DastSortBy.SCAN_TYPE.value == "scantype"


def test_get_environments_with_sort():
    # Enum entry → defaults to :asc
    asc = get_environments(sort=[DastSortBy.CREATED])
    # Raw "<col>:desc" string escape-hatch in the same list
    desc = get_environments(sort=["created:desc"])
    if len(asc.environments) >= 2 and len(desc.environments) >= 2:
        assert asc.environments[0].created <= asc.environments[-1].created
        assert desc.environments[0].created >= desc.environments[-1].created
        # asc and desc should reverse the relative order of the extremes
        assert asc.environments[0].environment_id == desc.environments[-1].environment_id
