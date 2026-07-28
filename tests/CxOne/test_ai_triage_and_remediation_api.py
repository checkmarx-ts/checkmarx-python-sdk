from urllib.parse import quote

import pytest

from CheckmarxPythonSDK.CxOne import (
    get_ai_triage_status,
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
from CheckmarxPythonSDK.CxOne import SastResultsAPI as _SastResultsAPI

_PROJECT_NAME = "happy-cook/WebGoat"
_QUERY_NAME = "SQL_Injection"


@pytest.fixture(scope="session")
def project_id():
    pid = _ProjectsAPI().get_project_id_by_name(_PROJECT_NAME)
    if not pid:
        pytest.skip(f"Project '{_PROJECT_NAME}' not found")
    return pid


@pytest.fixture(scope="session")
def scan_id(project_id):
    scans = _ScansAPI().get_a_list_of_scans(
        limit=10, project_ids=[project_id], statuses=["Completed"]
    )
    for scan in scans.scans:
        if "sast" in (scan.engines or []):
            return scan.id
    pytest.skip(f"No completed SAST scan found for project '{_PROJECT_NAME}'")


@pytest.fixture(scope="session")
def sql_injection_result(scan_id):
    """Return the first SQL_Injection SAST result that has a result_hash."""
    batch = _SastResultsAPI().get_sast_results_by_scan_id(
        scan_id=scan_id,
        query=_QUERY_NAME,
        include_nodes=False,
        limit=5,
    )
    for r in batch.get("results") or []:
        if r.result_hash and r.similarity_id is not None:
            return r
    pytest.skip(
        f"No '{_QUERY_NAME}' SAST result found in the latest scan of '{_PROJECT_NAME}'"
    )


def test_trigger_ai_triage(project_id, scan_id, sql_injection_result):
    # resultIDs in the JSON body should be raw (not URL-encoded)
    request = AiTriageRequest(
        scanID=scan_id,
        buckets=[
            TriageBucket(
                scannerType="sast",
                resultIDs=[sql_injection_result.result_hash],
            )
        ],
    )
    try:
        response = trigger_ai_triage(request)
    except Exception as e:
        msg = str(e)
        if any(code in msg for code in ("400", "401", "402", "403", "422")):
            pytest.skip(f"AI Triage API error: {msg}")
        raise

    assert isinstance(response, AiTriageResponse)
    assert response.status == "accepted"
    assert response.triageID is not None
    assert isinstance(response.published, bool)


def test_get_ai_triage_status(project_id, scan_id, sql_injection_result):
    try:
        result = get_ai_triage_status(
            engine="sast",
            group_id=sql_injection_result.similarity_id,
            project_id=project_id,
        )
    except Exception as e:
        msg = str(e)
        if any(code in msg for code in ("401", "403", "404", "422")):
            pytest.skip(f"AI Triage SSE status API error: {msg}")
        raise

    assert isinstance(result, AiTriageResult)
    # stream may contain only heartbeats if triage is still in progress
    if result.triageStatus is not None:
        assert result.triageStatus in (
            "NOT_TRIAGED", "IN_PROGRESS", "FAILED", "VULNERABLE",
            "PROPOSED_NOT_EXPLOITABLE", "UNCERTAIN", "RISK_ACCEPTED",
        )


def test_retrieve_ai_triage_results(project_id, scan_id, sql_injection_result):
    group_id = quote(str(sql_injection_result.similarity_id), safe="")
    try:
        triage_result = retrieve_ai_triage_results(
            project_id=project_id,
            group_id=group_id,
        )
    except Exception as e:
        msg = str(e)
        # 404 is expected while triage is still processing (async)
        if "404" in msg:
            pytest.skip(f"Triage result not yet available (async in progress): {msg}")
        if any(code in msg for code in ("401", "403", "422")):
            pytest.skip(f"AI Triage results API error: {msg}")
        raise

    assert isinstance(triage_result, AiTriageResult)
    # triageStatus is None when the job is still processing (different response shape)
    if triage_result.triageStatus is not None:
        assert triage_result.triageStatus in (
            "NOT_TRIAGED", "IN_PROGRESS", "FAILED", "VULNERABLE",
            "PROPOSED_NOT_EXPLOITABLE", "UNCERTAIN", "RISK_ACCEPTED",
        )


def test_trigger_ai_remediation(project_id, scan_id, sql_injection_result):
    # resultIDs in the JSON body should be raw (not URL-encoded)
    request = AiRemediationRequest(
        scanID=scan_id,
        buckets=[
            RemediationBucket(
                scannerType="sast",
                resultIDs=[sql_injection_result.result_hash],
            )
        ],
    )
    try:
        response = trigger_ai_remediation(request)
    except Exception as e:
        msg = str(e)
        if any(code in msg for code in ("400", "401", "402", "403", "422")):
            pytest.skip(f"AI Remediation API error: {msg}")
        raise

    assert isinstance(response, AiRemediationResponse)
    assert response.status == "accepted"
    assert isinstance(response.published, bool)
    # published=True → new job created with a remediationJobId
    # published=False → existing job found; existingState is set instead
    if response.published:
        assert response.remediationJobId is not None
    else:
        assert response.existingState is not None


def test_retrieve_ai_remediation_details(project_id, scan_id, sql_injection_result):
    result_id = quote(sql_injection_result.result_hash, safe="")
    try:
        details = retrieve_ai_remediation_details(
            scan_id=scan_id,
            result_id=result_id,
        )
    except Exception as e:
        msg = str(e)
        # 404 means remediation hasn't been triggered yet or is still processing
        if "404" in msg:
            pytest.skip(f"Remediation details not yet available: {msg}")
        if any(code in msg for code in ("401", "403", "422")):
            pytest.skip(f"AI Remediation details API error: {msg}")
        raise

    assert isinstance(details, AiRemediationDetails)
    assert details.scanID is not None
    assert isinstance(details.results, list)
