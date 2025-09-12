from CheckmarxPythonSDK.CxOne import (
    get_all_custom_states,
    create_a_custom_state,
    delete_a_custom_state,
)


def test_get_all_custom_states():
    custom_state = get_all_custom_states()
    assert custom_state is not None


def test_create_a_custom_state():
    response = create_a_custom_state(name="SNOOZE_RESULT")
    assert response is not None


def test_delete_a_custom_state():
    custom_state_id = get_all_custom_states()[0].id
    response = delete_a_custom_state(custom_state_id=custom_state_id)
    assert response is not None
