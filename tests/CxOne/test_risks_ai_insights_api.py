import pytest

from CheckmarxPythonSDK.CxOne import get_risks_ai_insights, ProjectsAPI as _ProjectsAPI
from CheckmarxPythonSDK.CxOne.dto import (
    AiTriageInsight,
    RemediationInsight,
    RisksAiInsightsResponse,
    RiskWithAiInsights,
)

_PROJECT_NAME = "happy-cook/WebGoat"


@pytest.fixture(scope="session")
def project_id():
    pid = _ProjectsAPI().get_project_id_by_name(_PROJECT_NAME)
    if not pid:
        pytest.skip(f"Project '{_PROJECT_NAME}' not found")
    return pid


def test_get_risks_ai_insights(project_id):
    response = get_risks_ai_insights(project_id=project_id, limit=5)

    assert isinstance(response, RisksAiInsightsResponse)
    assert response.metaData is not None
    assert isinstance(response.metaData.totalResults, int)
    assert isinstance(response.metaData.filteredResults, int)
    assert isinstance(response.risks, list)


def test_get_risks_ai_insights_filter_by_engine(project_id):
    response = get_risks_ai_insights(
        project_id=project_id,
        engine=["SAST"],
        limit=5,
    )

    assert isinstance(response, RisksAiInsightsResponse)
    for risk in response.risks:
        assert isinstance(risk, RiskWithAiInsights)
        assert risk.engine == "SAST"
        assert risk.id is not None
        assert risk.riskName is not None


def test_get_risks_ai_insights_filter_by_ai_triage_status(project_id):
    response = get_risks_ai_insights(
        project_id=project_id,
        ai_triage_status=["VULNERABLE", "PROPOSED_NOT_EXPLOITABLE"],
        limit=10,
    )

    assert isinstance(response, RisksAiInsightsResponse)
    for risk in response.risks:
        assert risk.aiTriage is not None
        assert isinstance(risk.aiTriage, AiTriageInsight)
        assert risk.aiTriage.triageStatus in ("VULNERABLE", "PROPOSED_NOT_EXPLOITABLE")


def test_get_risks_ai_insights_filter_by_remediation_status(project_id):
    response = get_risks_ai_insights(
        project_id=project_id,
        remediation_status=["COMPLETED"],
        limit=5,
    )

    assert isinstance(response, RisksAiInsightsResponse)
    for risk in response.risks:
        assert risk.remediation is not None
        assert isinstance(risk.remediation, RemediationInsight)
        assert risk.remediation.status == "COMPLETED"


def test_get_risks_ai_insights_dto_fields(project_id):
    response = get_risks_ai_insights(
        project_id=project_id,
        engine=["SAST"],
        limit=3,
    )

    assert isinstance(response, RisksAiInsightsResponse)
    if not response.risks:
        pytest.skip("No SAST risks with AI insights found")

    risk = response.risks[0]
    assert isinstance(risk, RiskWithAiInsights)
    assert risk.projectId == project_id
    assert risk.severity in ("CRITICAL", "HIGH", "MEDIUM", "LOW", "INFO", None)
    assert risk.state in (
        "TO_VERIFY",
        "NOT_EXPLOITABLE",
        "PROPOSED_NOT_EXPLOITABLE",
        "CONFIRMED",
        "URGENT",
        None,
    )
    if risk.aiTriage is not None:
        assert isinstance(risk.aiTriage, AiTriageInsight)
    if risk.remediation is not None:
        assert isinstance(risk.remediation, RemediationInsight)
