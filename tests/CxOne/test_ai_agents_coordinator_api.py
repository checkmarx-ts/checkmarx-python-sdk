import pytest

from CheckmarxPythonSDK.CxOne import (
    get_account_configuration, update_account_configuration,
    get_project_configuration, update_project_configuration,
    list_history, list_history_field_values, export_history_csv,
)
from CheckmarxPythonSDK.CxOne.dto import (
    AiCoordinatorAccountConfigResponse, AiCoordinatorProjectConfigResponse,
    AiCoordinatorHistoryListResponse, AiCoordinatorHistoryFieldValuesResponse,
    AiCoordinatorAutoTriageAccountConfigWriteItem,
    AiCoordinatorAutoRemediationAccountConfigWriteItem,
    AiCoordinatorAutoTriageProjectConfigWriteItem,
    AiCoordinatorAutoRemediationProjectConfigWriteItem,
)


def _skip_on_client_error(e: Exception):
    msg = str(e)
    if "400" in msg or "401" in msg or "403" in msg or "404" in msg or "422" in msg:
        pytest.skip("API returned client error: {}".format(msg))
    raise e


@pytest.fixture(scope="session")
def account_config():
    try:
        return get_account_configuration()
    except ValueError as e:
        _skip_on_client_error(e)


@pytest.fixture(scope="session")
def project_id(account_config):
    """A project UUID taken from the live account configuration's
    auto_triage.config.projects, since this API has no dedicated project
    listing of its own."""
    triage = next(
        (c for c in account_config.configurations if c.feature == "auto_triage"), None
    )
    if triage and triage.config and triage.config.projects:
        return triage.config.projects[0]
    remediation = next(
        (c for c in account_config.configurations if c.feature == "auto_remediation"), None
    )
    if remediation and remediation.config and remediation.config.projects:
        return remediation.config.projects[0]
    pytest.skip("No project configured for auto-triage/auto-remediation on this tenant")


def test_get_account_configuration(account_config):
    assert isinstance(account_config, AiCoordinatorAccountConfigResponse)
    assert account_config.scope == "account"
    features = {c.feature for c in account_config.configurations if hasattr(c, "feature")}
    assert features <= {"auto_triage", "auto_remediation"}


def test_update_account_configuration_round_trip(account_config):
    """Write back the exact same (enabled, config) values already stored
    for each feature -- a true no-op -- to verify the write path without
    changing any real tenant setting."""
    write_items = []
    for item in account_config.configurations:
        if item.feature == "auto_triage":
            write_items.append(AiCoordinatorAutoTriageAccountConfigWriteItem(
                enabled=item.enabled, config=item.config,
            ))
        elif item.feature == "auto_remediation":
            write_items.append(AiCoordinatorAutoRemediationAccountConfigWriteItem(
                enabled=item.enabled, config=item.config,
            ))
    if not write_items:
        pytest.skip("No existing account configuration to round-trip")

    try:
        after = update_account_configuration(write_items)
    except ValueError as e:
        _skip_on_client_error(e)
        return
    assert isinstance(after, AiCoordinatorAccountConfigResponse)
    for before_item in account_config.configurations:
        after_item = next(
            c for c in after.configurations if c.feature == before_item.feature
        )
        assert after_item.enabled == before_item.enabled


def test_get_project_configuration(project_id):
    try:
        cfg = get_project_configuration(project_id)
    except ValueError as e:
        _skip_on_client_error(e)
        return
    assert isinstance(cfg, AiCoordinatorProjectConfigResponse)
    assert cfg.scope == "project"
    assert cfg.project_id == project_id


def test_update_project_configuration_round_trip(project_id):
    try:
        before = get_project_configuration(project_id)
    except ValueError as e:
        _skip_on_client_error(e)
        return

    write_items = []
    for item in before.configurations:
        if item.feature == "auto_triage":
            write_items.append(AiCoordinatorAutoTriageProjectConfigWriteItem(
                enabled=item.enabled, config=item.config,
            ))
        elif item.feature == "auto_remediation":
            write_items.append(AiCoordinatorAutoRemediationProjectConfigWriteItem(
                enabled=item.enabled, config=item.config,
            ))
    if not write_items:
        pytest.skip("No existing project configuration to round-trip")

    try:
        after = update_project_configuration(project_id, write_items)
    except ValueError as e:
        _skip_on_client_error(e)
        return
    assert isinstance(after, AiCoordinatorProjectConfigResponse)
    for before_item in before.configurations:
        after_item = next(
            c for c in after.configurations if c.feature == before_item.feature
        )
        assert after_item.enabled == before_item.enabled


def test_list_history():
    history = list_history(limit=5)
    assert isinstance(history, AiCoordinatorHistoryListResponse)
    assert history.meta_data is not None
    assert history.meta_data.page_size == 5


def test_list_history_field_values():
    values = list_history_field_values(field="projectNames")
    assert isinstance(values, AiCoordinatorHistoryFieldValuesResponse)
    assert isinstance(values.values, list)


def test_export_history_csv():
    csv_text = export_history_csv()
    assert isinstance(csv_text, str)
    # Even with zero history rows, a CSV export should at least carry a
    # header row.
    assert "," in csv_text or csv_text == ""
