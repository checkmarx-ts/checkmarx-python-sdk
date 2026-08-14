import pytest

from CheckmarxPythonSDK.CxOne import get_risks, ProjectsAPI as _ProjectsAPI
from CheckmarxPythonSDK.CxOne.dto import RisksResponse, Risk

_PROJECT_NAME = "happy-cook/WebGoat"


@pytest.fixture(scope="session")
def project_id():
    pid = _ProjectsAPI().get_project_id_by_name(_PROJECT_NAME)
    if not pid:
        pytest.skip(f"Project '{_PROJECT_NAME}' not found")
    return pid


def test_get_risks(project_id):
    response = get_risks(project_id=project_id, limit=5)

    assert isinstance(response, RisksResponse)
    assert response.metaData is not None
    assert isinstance(response.metaData.totalResults, int)
    assert isinstance(response.metaData.filteredResults, int)
    assert isinstance(response.risks, list)


def test_get_risks_filter_by_engine(project_id):
    response = get_risks(project_id=project_id, engine=["SAST"], limit=5)

    assert isinstance(response, RisksResponse)
    for risk in response.risks:
        assert isinstance(risk, Risk)
        assert risk.engine == "SAST"
        assert risk.id is not None
        assert risk.riskName is not None
        assert risk.groupId is not None


def test_get_risks_filter_by_severity(project_id):
    response = get_risks(
        project_id=project_id,
        engine=["SAST"],
        severity=["CRITICAL", "HIGH"],
        limit=5,
    )

    assert isinstance(response, RisksResponse)
    for risk in response.risks:
        assert risk.severity in ("CRITICAL", "HIGH")


def test_get_risks_filter_by_state(project_id):
    response = get_risks(
        project_id=project_id,
        state=["CONFIRMED", "URGENT"],
        limit=5,
    )

    assert isinstance(response, RisksResponse)
    for risk in response.risks:
        assert risk.state in ("CONFIRMED", "URGENT")
