from CheckmarxPythonSDK.CxRestAPISDK import GeneralAPI
from CheckmarxPythonSDK.CxRestAPISDK.sast.general.dto import CxTranslationInput, CxUserPersistence


def test_get_server_license_data():
    result = GeneralAPI().get_server_license_data()
    assert result is not None


def test_get_server_system_version():
    result = GeneralAPI().get_server_system_version()
    assert result is not None


def test_get_result_states():
    result = GeneralAPI().get_result_states()
    assert result is not None


def test_create_update_delete_result_state():
    api = GeneralAPI()
    state_id = api.create_result_state(
        translation_inputs=[CxTranslationInput(language_id=1033, name="TestStateCustom")],
        permission="set-result-state-confirmed",
    )
    assert state_id > 4

    result = api.update_result_state(
        state_id=state_id,
        translation_inputs=[CxTranslationInput(language_id=1033, name="TestStateUpdated")],
        permission="set-result-state-confirmed",
    )
    assert result is True

    result = api.delete_result_state(state_id=state_id)
    assert result is True


def test_get_all_scheduled_jobs():
    result = GeneralAPI().get_all_scheduled_jobs()
    assert result is not None


def test_get_user_persistence_data_for_current_user():
    result = GeneralAPI().get_user_persistence_data_for_current_user(persistence_keys=["key1", "key2"])
    assert result is not None


def test_update_persistence_data_for_current_user():
    result = GeneralAPI().update_persistence_data_for_current_user(
        [CxUserPersistence("key1", "value1"), CxUserPersistence("key2", "value2")]
    )
    assert result is True


def test_get_audit_trail_for_roles():
    result = GeneralAPI().get_audit_trail_for_roles(from_date="2020-01-01", to_date="2030-01-01")
    assert result is not None


def test_get_audit_trail_for_teams():
    result = GeneralAPI().get_audit_trail_for_teams(from_date="2020-01-01", to_date="2030-01-01")
    assert result is not None


def test_get_teams_trail_for_presets():
    result = GeneralAPI().get_audit_trail_for_presets(from_date="2020-01-01", to_date="2030-01-01")
    assert result is not None


def test_get_teams_trail_for_results():
    result = GeneralAPI().get_audit_trail_for_results(from_date="2020-01-01", to_date="2030-01-01")
    assert result is not None
