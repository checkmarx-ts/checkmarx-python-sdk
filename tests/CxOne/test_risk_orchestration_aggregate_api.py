import pytest

from CheckmarxPythonSDK.CxOne import get_risks_aggregate, ProjectsAPI as _ProjectsAPI
from CheckmarxPythonSDK.CxOne.dto import RiskCounter, RisksAggregateResponse

_PROJECT_NAME = "happy-cook/WebGoat"

_VALID_SEVERITIES = {"CRITICAL", "HIGH", "MEDIUM", "LOW", "INFO", ""}
_VALID_ENGINES = {"SAST", "IAC", "SCA", ""}


@pytest.fixture(scope="session")
def project_id():
    pid = _ProjectsAPI().get_project_id_by_name(_PROJECT_NAME)
    if not pid:
        pytest.skip(f"Project '{_PROJECT_NAME}' not found")
    return pid


def test_get_risks_aggregate_by_severity(project_id):
    response = get_risks_aggregate(
        project_id=project_id,
        group_by=["severity"],
    )

    assert isinstance(response, RisksAggregateResponse)
    assert isinstance(response.risksCounters, list)
    for counter in response.risksCounters:
        assert isinstance(counter, RiskCounter)
        assert counter.severity in _VALID_SEVERITIES
        assert isinstance(counter.count, int)
        assert counter.count >= 0


def test_get_risks_aggregate_by_engine(project_id):
    response = get_risks_aggregate(
        project_id=project_id,
        group_by=["engine"],
    )

    assert isinstance(response, RisksAggregateResponse)
    for counter in response.risksCounters:
        assert counter.engine in _VALID_ENGINES
        assert isinstance(counter.count, int)


def test_get_risks_aggregate_by_severity_and_engine(project_id):
    response = get_risks_aggregate(
        project_id=project_id,
        group_by=["severity", "engine"],
    )

    assert isinstance(response, RisksAggregateResponse)
    assert len(response.risksCounters) >= 1
    for counter in response.risksCounters:
        assert counter.severity in _VALID_SEVERITIES
        assert counter.engine in _VALID_ENGINES


def test_get_risks_aggregate_filter_by_engine(project_id):
    response = get_risks_aggregate(
        project_id=project_id,
        group_by=["severity"],
        engine=["SAST"],
    )

    assert isinstance(response, RisksAggregateResponse)
    total = sum(c.count for c in response.risksCounters if c.count)
    assert total >= 0
