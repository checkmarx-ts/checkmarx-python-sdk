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


def test_create_result_state():
    result = GeneralAPI().create_result_state(
        translation_inputs=[CxTranslationInput(language_id=1033, name="DoesNotMakeSense")],
        permission="set-result-state-nonsense"
    )
    assert result > 4


def test_update_result_state():
    result = GeneralAPI().update_result_state(
        state_id=5,
        translation_inputs=[CxTranslationInput(language_id=1033, name="DoesNotMakeSense")],
        permission="set-result-state-nonsense"
    )
    assert result is True


def test_delete_result_state():
    result = GeneralAPI().delete_result_state(state_id=5)
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
    result = GeneralAPI().get_audit_trail_for_roles(from_date="2024-01-01", to_date="2024-07-17")
    assert result is not None


def test_get_teams_trail_for_roles():
    result = GeneralAPI().get_audit_trail_for_teams(from_date="2024-01-01", to_date="2024-07-17")
    assert result is not None
