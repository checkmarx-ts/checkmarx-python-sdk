from CheckmarxPythonSDK.utilities.configUtility import get_config


def test_env_timeout_is_converted_to_int(monkeypatch):
    """An env-var timeout must reach Configuration as int, not str.

    Regression guard for the bug where cxsca_timeout=120 produced the str
    '120' and httpx later failed with
    TypeError: an integer is required (got type str) in socket.settimeout().
    """
    monkeypatch.setenv("cxsca_timeout", "120")

    config = get_config(
        config_default={"timeout": 60},
        section="CxSCA",
        prefix="cxsca_",
    )

    assert config["timeout"] == 120
    assert isinstance(config["timeout"], int)


def test_env_timeout_upper_case_is_converted_to_int(monkeypatch):
    monkeypatch.setenv("CXSCA_TIMEOUT", "90")

    config = get_config(
        config_default={"timeout": 60},
        section="CxSCA",
        prefix="cxsca_",
    )

    assert config["timeout"] == 90
    assert isinstance(config["timeout"], int)


def test_env_verify_false_is_converted_to_bool(monkeypatch):
    monkeypatch.setenv("cxsca_verify", "false")

    config = get_config(
        config_default={"verify": True},
        section="CxSCA",
        prefix="cxsca_",
    )

    assert config["verify"] is False


def test_default_timeout_when_env_absent(monkeypatch):
    monkeypatch.delenv("cxsca_timeout", raising=False)
    monkeypatch.delenv("CXSCA_TIMEOUT", raising=False)
    # Point at a nonexistent ini so the local ~/.Checkmarx/config.ini
    # cannot supply values; only the default should remain.
    monkeypatch.setenv("checkmarx_config_path", "no_such_config.ini")

    config = get_config(
        config_default={"timeout": 60},
        section="CxSCA",
        prefix="cxsca_",
    )

    assert config["timeout"] == 60
    assert isinstance(config["timeout"], int)
