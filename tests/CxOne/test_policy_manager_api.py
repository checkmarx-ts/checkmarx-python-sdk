import pytest

from CheckmarxPythonSDK.CxOne import (
    assign_projects_to_policy,
    create_policy,
    create_policy_v2,
    delete_policies,
    delete_policy,
    delete_projects_from_policy,
    get_default_policy,
    get_enhanced_incidents_with_pagination_and_filters,
    get_evaluated_policies_by_scan_id_and_project_id,
    get_policy,
    get_policy_v2,
    get_policy_violations,
    get_projects_tags,
    get_tenant_incidents,
    get_tenant_incidents_total_count,
    get_tenant_incidents_with_pagination,
    get_tenant_incidents_with_pagination_and_filters,
    get_tenant_policies,
    get_tenant_policies_with_pagination,
    get_tenant_policies_with_pagination_v3,
    get_tenant_projects,
    pin_policy,
    update_policy,
    update_policy_v2,
)
from CheckmarxPythonSDK.CxOne import ScansAPI as _ScansAPI
from CheckmarxPythonSDK.CxOne.dto import (
    IncidentsPaginationDto,
    PoliciesPaginationDto,
    PolicyViolationWebDto,
    PolicyWebDto,
    ProjectsInPolicyDto,
    ProjectWebDto,
)

_TEST_POLICY_NAME = "sdk-test-policy-delete-me"


def _skip_on_client_error(e: Exception):
    msg = str(e)
    if "400" in msg or "401" in msg or "403" in msg or "404" in msg:
        pytest.skip("API returned client error: {}".format(msg))
    raise e


@pytest.fixture
def temp_policy():
    """Create a throwaway policy for a test, and delete it afterwards."""
    try:
        policy_id = create_policy(PolicyWebDto(name=_TEST_POLICY_NAME))
    except Exception as e:
        _skip_on_client_error(e)
        return
    try:
        yield policy_id
    finally:
        delete_policy(policy_id)


@pytest.fixture(scope="session")
def completed_scan():
    """A recently completed scan, for the per-scan endpoints."""
    try:
        scans = _ScansAPI().get_a_list_of_scans(
            limit=1, offset=0, statuses=["Completed"]
        )
    except Exception as e:
        pytest.skip("Could not list scans: {}".format(e))
        return
    if not scans.scans:
        pytest.skip("No completed scans found")
    return scans.scans[0]


# ---- Policies ----


def test_get_tenant_policies():
    policies = get_tenant_policies()
    assert isinstance(policies, list)
    for p in policies:
        assert isinstance(p, PolicyWebDto)
        assert p.id is not None
        assert p.name is not None


def test_get_tenant_policies_with_pagination():
    result = get_tenant_policies_with_pagination(limit=5, page=1)
    assert isinstance(result, PoliciesPaginationDto)
    assert isinstance(result.filteredPoliciesCount, int)
    assert len(result.policies) <= 5


def test_get_tenant_policies_with_pagination_v3():
    result = get_tenant_policies_with_pagination_v3(limit=5, page=1)
    assert isinstance(result, PoliciesPaginationDto)
    assert isinstance(result.filteredPoliciesCount, int)


def test_get_default_policy():
    # May legitimately be None if the tenant has no default policy set.
    result = get_default_policy()
    assert result is None or result.id is not None


def test_create_get_update_delete_policy_lifecycle():
    policy_id = create_policy(PolicyWebDto(name=_TEST_POLICY_NAME))
    try:
        policy = get_policy(policy_id)
        assert isinstance(policy, PolicyWebDto)
        assert policy.id == policy_id
        assert policy.name == _TEST_POLICY_NAME

        policy.description = "updated by test"
        assert update_policy(policy_id, policy) == policy_id

        updated = get_policy_v2(policy_id)
        assert updated.description == "updated by test"

        assert update_policy_v2(policy_id, updated) == policy_id
    finally:
        assert delete_policy(policy_id) is True


def test_create_policy_v2_and_bulk_delete():
    policy_id = create_policy_v2(PolicyWebDto(name=_TEST_POLICY_NAME + "-v2"))
    assert isinstance(policy_id, int)
    assert delete_policies([policy_id]) is True


def test_pin_policy(temp_policy):
    assert pin_policy(temp_policy, True) == temp_policy
    assert get_policy(temp_policy).pinPolicy is True
    assert pin_policy(temp_policy, False) == temp_policy
    assert get_policy(temp_policy).pinPolicy is False


def test_assign_and_remove_projects(temp_policy):
    projects = get_tenant_projects()
    if not projects:
        pytest.skip("No projects available on this tenant")
    target = ProjectWebDto(astProjectId=projects[0].astProjectId, name=projects[0].name)

    assert (
        assign_projects_to_policy(
            temp_policy, ProjectsInPolicyDto(projects=[target], id=temp_policy)
        )
        == temp_policy
    )
    assert any(
        p.astProjectId == target.astProjectId
        for p in get_policy(temp_policy).projects
    )

    assert (
        delete_projects_from_policy(
            temp_policy, ProjectsInPolicyDto(projects=[target], id=temp_policy)
        )
        is True
    )
    assert get_policy(temp_policy).projects == []


# ---- Projects ----


def test_get_tenant_projects():
    projects = get_tenant_projects()
    assert isinstance(projects, list)
    for p in projects:
        assert isinstance(p, ProjectWebDto)
        assert p.astProjectId is not None


def test_get_projects_tags():
    tags = get_projects_tags()
    assert isinstance(tags, list)


# ---- Incidents ----


def test_get_tenant_incidents():
    result = get_tenant_incidents()
    assert isinstance(result, IncidentsPaginationDto)
    assert isinstance(result.filteredIncidentsCount, int)


def test_get_tenant_incidents_total_count():
    count = get_tenant_incidents_total_count()
    assert isinstance(count, int)
    assert count >= 0


def test_get_tenant_incidents_with_pagination():
    result = get_tenant_incidents_with_pagination(limit=5, page=1)
    assert isinstance(result, IncidentsPaginationDto)


def test_get_tenant_incidents_with_pagination_and_filters():
    result = get_tenant_incidents_with_pagination_and_filters(limit=5, page=1)
    assert isinstance(result, IncidentsPaginationDto)


def test_get_enhanced_incidents_with_pagination_and_filters():
    try:
        result = get_enhanced_incidents_with_pagination_and_filters(limit=5, page=1)
    except Exception as e:
        _skip_on_client_error(e)
        return
    assert isinstance(result.filteredIncidentsCount, int)


def test_get_incident_results():
    result = get_tenant_incidents()
    if not result.incidents:
        pytest.skip("No incidents on this tenant to fetch results for")
    from CheckmarxPythonSDK.CxOne import get_incident_results
    from CheckmarxPythonSDK.CxOne.dto import IncidentResultsDTO

    incident_results = get_incident_results(result.incidents[0].id, limit=5, page=1)
    assert isinstance(incident_results, IncidentResultsDTO)


# ---- Policy violations / evaluation (require a scan a policy has evaluated) ----


def test_get_policy_violations(completed_scan):
    try:
        result = get_policy_violations(
            project_id=completed_scan.project_id, scan_id=completed_scan.id
        )
    except Exception as e:
        _skip_on_client_error(e)
        return
    assert isinstance(result, PolicyViolationWebDto)


def test_get_evaluated_policies_by_scan_id_and_project_id(completed_scan):
    try:
        result = get_evaluated_policies_by_scan_id_and_project_id(
            scan_id=completed_scan.id, ast_project_id=completed_scan.project_id
        )
    except Exception as e:
        _skip_on_client_error(e)
        return
    assert result.status in ("COMPLETED", "NONE", "EVALUATING")


# Note: delete_data() / delete_data_for_service() are not exercised here --
# they delete data-retention records across services tenant-wide and are
# not something a test should run against a real tenant.
