import json
import tempfile
import time

import pytest

from CheckmarxPythonSDK.CxOne import (
    create_environment, delete_environment,
    create_auth_session, update_auth_session_api_file,
    validate_auth_session_api_file, bulk_replace_auth_session_api_files,
    update_auth_session_credentials, update_auth_session_file,
    get_auth_session, get_auth_session_api_file, delete_auth_session_api_file,
    get_auth_session_api_files_data, get_auth_session_diagnostics,
    get_auth_session_domains, get_auth_session_masked, set_auth_session_no_auth,
    ping_auth_session, update_auth_session_report, get_auth_session_report,
    get_auth_session_report_data, get_auth_session_state,
    get_auth_session_test_log,
)
from CheckmarxPythonSDK.CxOne.dto import (
    DastEnvironmentInput, DastScanType, DastAuthSession,
    DastAuthSessionCredentials, DastApiFileWithType,
)


def _skip_on_client_error(e: Exception):
    msg = str(e)
    if "400" in msg or "401" in msg or "403" in msg or "404" in msg:
        pytest.skip("API returned client error: {}".format(msg))
    raise e


@pytest.fixture
def env_id():
    """A throwaway Environment to drive an auth session on."""
    eid = create_environment(DastEnvironmentInput(
        domain=f"sdk-authsession-{int(time.time())}",
        url="https://example.com",
        scan_type=DastScanType.DAST,
    ))
    try:
        yield eid
    finally:
        delete_environment(eid)


@pytest.fixture
def auth_session_uuid(env_id):
    """Create an auth session on `env_id` ("CLI" is the one confirmed-
    valid SessionType value — see create_auth_session's docstring),
    settle it to NO_AUTH, and return its uuid.

    The settle step matters: confirmed live, a session fresh off
    create_auth_session accepts file uploads/returns a file id, but the
    file never actually attaches, and /diagnostics 404s — both work once
    *any* PUT has committed a method on the session first. See
    update_auth_session_api_file's docstring.
    """
    ok = create_auth_session(
        environment_id=env_id, session_type="CLI", url="https://example.com",
    )
    assert ok is True
    uuid = get_auth_session(env_id).uuid
    assert set_auth_session_no_auth(env_id, uuid) is True
    return uuid


@pytest.fixture
def openapi_file():
    path = tempfile.NamedTemporaryFile(suffix=".json", delete=False).name
    with open(path, "w") as f:
        json.dump({"openapi": "3.0.0", "info": {"title": "dummy", "version": "1.0"}, "paths": {}}, f)
    return path


def test_create_and_get_auth_session(env_id, auth_session_uuid):
    session = get_auth_session(env_id)
    assert isinstance(session, DastAuthSession)
    assert session.uuid == auth_session_uuid
    assert session.method == "NO_AUTH"  # default, before any credentials are set

    masked = get_auth_session_masked(env_id)
    assert isinstance(masked, DastAuthSession)
    assert masked.uuid == auth_session_uuid


def test_get_auth_session_state(env_id, auth_session_uuid):
    state = get_auth_session_state(env_id, auth_session_uuid)
    assert isinstance(state, str) and state


def test_ping_auth_session(env_id, auth_session_uuid):
    # "CLI" is the confirmed-valid Source value (see docstring). The
    # fixture already settles the session to NO_AUTH, i.e. "done" --
    # pinging a done session 409s rather than validation-failing,
    # confirming "CLI" is accepted as Source and this is a real state
    # check, not a rejected request.
    with pytest.raises(Exception) as exc_info:
        ping_auth_session(env_id, auth_session_uuid, source="CLI")
    assert "409" in str(exc_info.value) or "already done" in str(exc_info.value)


def test_update_auth_session_credentials(env_id, auth_session_uuid):
    ok = update_auth_session_credentials(
        uuid=auth_session_uuid,
        environment_id=env_id,
        login_page_url="https://example.com/login",
        user_name="testuser",
        password="testpass",
    )
    assert ok is True

    session = get_auth_session(env_id)
    assert session.method == "CREDENTIALS"
    assert isinstance(session.credentials, DastAuthSessionCredentials)
    assert session.credentials.user_name == "testuser"
    assert session.credentials.login_page_url == "https://example.com/login"


def test_get_auth_session_domains_requires_live_session(env_id, auth_session_uuid):
    # Confirmed live: this 404s for a session with no actively-connected
    # browser/CLI side -- it's not enough for the auth session record to
    # exist. There's no way to drive a real browser/CLI session from here,
    # so this only confirms the call shape; a populated response isn't
    # reachable from an automated test.
    try:
        domains = get_auth_session_domains(env_id, auth_session_uuid)
        assert isinstance(domains, list)
    except Exception as e:
        _skip_on_client_error(e)


def test_validate_auth_session_api_file(openapi_file):
    result = validate_auth_session_api_file(openapi_file, api_type="OPENAPI")
    assert result["valid"] is True


def test_update_and_delete_auth_session_api_file(env_id, auth_session_uuid, openapi_file):
    file_id = update_auth_session_api_file(
        uuid=auth_session_uuid, environment_id=env_id,
        api_file=openapi_file, api_type="OPENAPI",
    )
    assert isinstance(file_id, str) and file_id

    files = get_auth_session_api_files_data(env_id)
    assert isinstance(files, list)
    assert any(isinstance(f, DastApiFileWithType) and f.api_type == "OPENAPI" for f in files)

    content = get_auth_session_api_file(env_id)
    assert isinstance(content, bytes) and b"openapi" in content

    assert delete_auth_session_api_file(env_id, file_id) is True
    assert get_auth_session_api_files_data(env_id) == []


def test_bulk_replace_auth_session_api_files(env_id, openapi_file):
    file_ids = bulk_replace_auth_session_api_files(
        environment_id=env_id, files=[openapi_file], api_types=["OPENAPI"],
    )
    assert isinstance(file_ids, list) and len(file_ids) == 1

    files = get_auth_session_api_files_data(env_id)
    assert any(f.api_type == "OPENAPI" for f in files)


def test_update_auth_session_report_and_get_test_log(env_id, auth_session_uuid):
    log_path = tempfile.NamedTemporaryFile(suffix=".log", delete=False).name
    with open(log_path, "w") as f:
        f.write("dummy auth test log content\n")

    assert update_auth_session_report(env_id, auth_session_uuid, test_log=log_path) is True

    content = get_auth_session_test_log(env_id, auth_session_uuid)
    assert content == b"dummy auth test log content\n"

    # get_auth_session_report / get_auth_session_report_data derive their
    # response from a real report blob (produced by the DAST auth-test
    # tool), which a bare testLog upload doesn't provide -- confirmed live
    # to 500 ("failed to retrieve report") in that case. Not a bug in the
    # SDK; just not reachable without a real DAST auth-test run.
    with pytest.raises(Exception):
        get_auth_session_report(env_id, auth_session_uuid)
    with pytest.raises(Exception):
        get_auth_session_report_data(env_id, auth_session_uuid)


def test_get_auth_session_diagnostics(env_id, auth_session_uuid):
    archive = get_auth_session_diagnostics(env_id)
    assert isinstance(archive, bytes)
    assert archive[:2] == b"PK", f"expected ZIP magic, got {archive[:8]!r}"


def test_update_auth_session_file_rejects_non_zest_recording(env_id, auth_session_uuid):
    # RECORDING expects a real Zest (JSON) recording from a browser-based
    # capture tool, not an arbitrary file. Confirmed live: a non-Zest file
    # 500s with "failed to process ZST file: failed to unmarshal ZST JSON
    # content". There's no practical way to synthesize a valid Zest
    # recording here, so this just documents the constraint.
    recording_path = tempfile.NamedTemporaryFile(suffix=".zst", delete=False).name
    with open(recording_path, "w") as f:
        f.write("not a real zest recording\n")

    with pytest.raises(Exception) as exc_info:
        update_auth_session_file(
            uuid=auth_session_uuid, environment_id=env_id, method="RECORDING",
            recording_file=recording_path,
        )
    assert "500" in str(exc_info.value) or "ZST" in str(exc_info.value)
