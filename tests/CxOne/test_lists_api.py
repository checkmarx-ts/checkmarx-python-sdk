from CheckmarxPythonSDK.CxOne import (
    get_severities,
    get_states,
    get_statuses,
)


def test_get_severities():
    result = get_severities()
    assert result is not None
    assert isinstance(result, list)
    assert "HIGH" in result


def test_get_states():
    result = get_states()
    assert result is not None
    assert isinstance(result, list)
    assert "CONFIRMED" in result


def test_get_statuses():
    result = get_statuses()
    assert result is not None
    assert isinstance(result, list)
    assert "NEW" in result
