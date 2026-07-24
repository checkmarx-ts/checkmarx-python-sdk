from urllib.parse import quote

import pytest

from CheckmarxPythonSDK.CxOne import (
    trigger_ai_triage,
    retrieve_ai_triage_results,
    trigger_ai_remediation,
    retrieve_ai_remediation_details,
)
from CheckmarxPythonSDK.CxOne.dto import (
    AiTriageRequest,
    AiTriageResponse,
    AiTriageResult,
    TriageBucket,
    AiRemediationRequest,
    AiRemediationResponse,
    AiRemediationDetails,
    RemediationBucket,
)
from CheckmarxPythonSDK.CxOne import ProjectsAPI as _ProjectsAPI
from CheckmarxPythonSDK.CxOne import ScansAPI as _ScansAPI
from CheckmarxPythonSDK.CxOne import ScannersResultsAPI as _ScannersResultsAPI


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


def _get_sast_result(scan_id):
    """Return the first SAST result that has an alternate_id."""
    results = _ScannersResultsAPI().get_all_scanners_results_by_scan_id(
        scan_id=scan_id, limit=5
    )
    for result in results.results or []:
        if result.type == "sast" and result.alternate_id and result.similarity_id:
            return result
    return None


def test_trigger_ai_triage():
    project_id = _get_project_id()
    if not project_id:
        pytest.skip("No projects found")
    scan_id = _get_sast_scan_id(project_id)
    if not scan_id:
        pytest.skip("No completed SAST scan found")
    result = _get_sast_result(scan_id)
    if not result:
        pytest.skip("No SAST result with alternateId found")

    request = AiTriageRequest(
        scanID=scan_id,
        buckets=[
            TriageBucket(
                scannerType="sast",
                resultIDs=[quote(result.alternate_id, safe="")],
            )
        ],
    )
    try:
        response = trigger_ai_triage(request)
    except Exception as e:
        msg = str(e)
        if any(code in msg for code in ("400", "401", "402", "403", "422")):
            pytest.skip(f"API returned client error: {msg}")
        raise

    assert isinstance(response, AiTriageResponse)
    assert response.status == "accepted"
    assert response.triageID is not None
    assert isinstance(response.published, bool)


def test_retrieve_ai_triage_results():
    project_id = _get_project_id()
    if not project_id:
        pytest.skip("No projects found")
    scan_id = _get_sast_scan_id(project_id)
    if not scan_id:
        pytest.skip("No completed SAST scan found")
    result = _get_sast_result(scan_id)
    if not result:
        pytest.skip("No SAST result with similarityId found")

    # For SAST, group_id is the similarityId (URL-encoded if needed)
    group_id = quote(result.similarity_id, safe="")

    try:
        triage_result = retrieve_ai_triage_results(
            project_id=project_id,
            group_id=group_id,
        )
    except Exception as e:
        msg = str(e)
        if any(code in msg for code in ("401", "403", "404", "422")):
            pytest.skip(f"API returned client error: {msg}")
        raise

    assert isinstance(triage_result, AiTriageResult)
    assert triage_result.triageStatus in (
        "NOT_TRIAGED", "IN_PROGRESS", "FAILED", "VULNERABLE",
        "PROPOSED_NOT_EXPLOITABLE", "UNCERTAIN", "RISK_ACCEPTED",
    )


def test_trigger_ai_remediation():
    project_id = _get_project_id()
    if not project_id:
        pytest.skip("No projects found")
    scan_id = _get_sast_scan_id(project_id)
    if not scan_id:
        pytest.skip("No completed SAST scan found")
    result = _get_sast_result(scan_id)
    if not result:
        pytest.skip("No SAST result with alternateId found")

    request = AiRemediationRequest(
        scanID=scan_id,
        buckets=[
            RemediationBucket(
                scannerType="sast",
                resultIDs=[quote(result.alternate_id, safe="")],
            )
        ],
    )
    try:
        response = trigger_ai_remediation(request)
    except Exception as e:
        msg = str(e)
        if any(code in msg for code in ("400", "401", "402", "403", "422")):
            pytest.skip(f"API returned client error: {msg}")
        raise

    assert isinstance(response, AiRemediationResponse)
    assert response.status == "accepted"
    assert response.remediationJobId is not None
    assert isinstance(response.published, bool)


def test_retrieve_ai_remediation_details():
    project_id = _get_project_id()
    if not project_id:
        pytest.skip("No projects found")
    scan_id = _get_sast_scan_id(project_id)
    if not scan_id:
        pytest.skip("No completed SAST scan found")
    result = _get_sast_result(scan_id)
    if not result:
        pytest.skip("No SAST result with alternateId found")

    result_id = quote(result.alternate_id, safe="")

    try:
        details = retrieve_ai_remediation_details(
            scan_id=scan_id,
            result_id=result_id,
        )
    except Exception as e:
        msg = str(e)
        if any(code in msg for code in ("401", "403", "404", "422")):
            pytest.skip(f"API returned client error: {msg}")
        raise

    assert isinstance(details, AiRemediationDetails)
    assert details.scanID is not None
    assert isinstance(details.results, list)
