import pytest

from CheckmarxPythonSDK.CxOne import (
    retrieve_process_status,
    trigger_ai_triage,
    trigger_ai_remediation,
)
from CheckmarxPythonSDK.CxOne.dto import (
    AiTriageTriggerRequest,
    AiTriageVulnerability,
)
from CheckmarxPythonSDK.CxOne import ProjectsAPI as _ProjectsAPI
from CheckmarxPythonSDK.CxOne import SastResultsAPI as _SastResultsAPI
from CheckmarxPythonSDK.CxOne import ScansAPI as _ScansAPI


def _get_project_id():
    projects = _ProjectsAPI().get_a_list_of_projects(limit=1)
    if projects.projects:
        return projects.projects[0].id
    return None


def _get_sast_scan_id(project_id):
    scans = _ScansAPI().get_a_list_of_scans(
        limit=5, project_ids=[project_id], statuses=["Completed"]
    )
    for scan in scans.scans:
        if "sast" in (scan.engines or []):
            return scan.id
    return None


def _get_sast_similarity_id(scan_id):
    results = _SastResultsAPI().get_sast_results_by_scan_id(
        scan_id=scan_id, limit=1, include_nodes=False
    )
    data = results.get("results", [])
    if data:
        return data[0].similarity_id
    return None


def test_trigger_ai_triage():
    project_id = _get_project_id()
    if not project_id:
        pytest.skip("No projects found")
    scan_id = _get_sast_scan_id(project_id)
    if not scan_id:
        pytest.skip("No completed SAST scan found")
    similarity_id = _get_sast_similarity_id(scan_id)
    if not similarity_id:
        pytest.skip("No SAST results found")

    request = AiTriageTriggerRequest(
        vulnerabilities=[
            AiTriageVulnerability(
                projectId=project_id,
                similarityId=similarity_id,
            )
        ]
    )
    try:
        response = trigger_ai_triage(request)
    except Exception as e:
        msg = str(e)
        if "400" in msg or "401" in msg or "403" in msg:
            pytest.skip("API returned client error: {}".format(msg))
        raise
    assert response is not None
    assert response.processId is not None
    assert response.status in ("in_progress", "rejected")


def test_trigger_ai_remediation():
    project_id = _get_project_id()
    if not project_id:
        pytest.skip("No projects found")
    scan_id = _get_sast_scan_id(project_id)
    if not scan_id:
        pytest.skip("No completed SAST scan found")
    similarity_id = _get_sast_similarity_id(scan_id)
    if not similarity_id:
        pytest.skip("No SAST results found")

    request = AiTriageTriggerRequest(
        vulnerabilities=[
            AiTriageVulnerability(
                projectId=project_id,
                similarityId=similarity_id,
            )
        ]
    )
    try:
        response = trigger_ai_remediation(request)
    except Exception as e:
        msg = str(e)
        if "400" in msg or "401" in msg or "403" in msg:
            pytest.skip("API returned client error: {}".format(msg))
        raise
    assert response is not None
    assert response.processId is not None
    assert response.status in ("in_progress", "rejected")


def test_retrieve_process_status():
    """Test retrieving process status after triggering an AI Triage.

    First triggers an AI Triage to obtain a valid processId, then polls
    the status endpoint.
    """
    project_id = _get_project_id()
    if not project_id:
        pytest.skip("No projects found")
    scan_id = _get_sast_scan_id(project_id)
    if not scan_id:
        pytest.skip("No completed SAST scan found")
    similarity_id = _get_sast_similarity_id(scan_id)
    if not similarity_id:
        pytest.skip("No SAST results found")

    request = AiTriageTriggerRequest(
        vulnerabilities=[
            AiTriageVulnerability(
                projectId=project_id,
                similarityId=similarity_id,
            )
        ]
    )
    try:
        trigger_response = trigger_ai_triage(request)
    except Exception as e:
        msg = str(e)
        if "400" in msg or "401" in msg or "403" in msg:
            pytest.skip("Trigger API returned client error: {}".format(msg))
        raise

    process_id = trigger_response.processId
    assert process_id is not None

    status_response = retrieve_process_status(process_id)
    assert status_response is not None
    assert status_response.processId == process_id
    assert status_response.status in (
        "in_progress",
        "completed",
        "completed_with_errors",
        "failed",
    )
    assert isinstance(status_response.results, list)
