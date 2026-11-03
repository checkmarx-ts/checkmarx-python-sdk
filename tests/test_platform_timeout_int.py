"""Regression guard: every platform's construct_configuration() must
return an int timeout, even when sourced as a string via env var.

Companion to tests/test_config_utility.py, which covers the shared
get_config() root cause. These tests cover the full per-platform call
chain end-to-end, including each platform's own defensive
int(config.get("timeout")) cast -- in case that cast is ever dropped
again, or a future config source (e.g. a quoted string in config.json)
bypasses the shared root-cause fix.
"""
from CheckmarxPythonSDK.CxScaApiSDK.config import (
    construct_configuration as cxsca_construct_configuration,
)
from CheckmarxPythonSDK.CxRestAPISDK.config import (
    construct_configuration as cxsast_construct_configuration,
)
from CheckmarxPythonSDK.CxReporting.config import (
    construct_configuration as cxreporting_construct_configuration,
)
from CheckmarxPythonSDK.CxODataApiSDK.config import (
    construct_configuration as cxodata_construct_configuration,
)
from CheckmarxPythonSDK.CxPortalSoapApiSDK.config import (
    construct_configuration as cxportal_construct_configuration,
)


def _isolate_from_local_config_file(monkeypatch):
    # Point at a nonexistent ini/json so the real ~/.Checkmarx/config.ini
    # on a developer's machine can't supply a competing value.
    monkeypatch.setenv("checkmarx_config_path", "no_such_config.ini")


def test_cxsca_timeout_is_int_from_env_var(monkeypatch):
    _isolate_from_local_config_file(monkeypatch)
    monkeypatch.setenv("cxsca_timeout", "120")
    configuration = cxsca_construct_configuration()
    assert configuration.timeout == 120
    assert isinstance(configuration.timeout, int)


def test_cxsast_timeout_is_int_from_env_var(monkeypatch):
    _isolate_from_local_config_file(monkeypatch)
    monkeypatch.setenv("cxsast_timeout", "90")
    configuration = cxsast_construct_configuration()
    assert configuration.timeout == 90
    assert isinstance(configuration.timeout, int)


def test_cxreporting_timeout_is_int_from_env_var(monkeypatch):
    _isolate_from_local_config_file(monkeypatch)
    monkeypatch.setenv("cxreporting_timeout", "75")
    configuration = cxreporting_construct_configuration()
    assert configuration.timeout == 75
    assert isinstance(configuration.timeout, int)


def test_cxodata_timeout_is_int_from_env_var(monkeypatch):
    _isolate_from_local_config_file(monkeypatch)
    monkeypatch.setenv("cxsast_timeout", "45")
    configuration = cxodata_construct_configuration()
    assert configuration.timeout == 45
    assert isinstance(configuration.timeout, int)


def test_cxportal_timeout_is_int_from_env_var(monkeypatch):
    _isolate_from_local_config_file(monkeypatch)
    monkeypatch.setenv("cxsast_timeout", "33")
    configuration = cxportal_construct_configuration()
    assert configuration.timeout == 33
    assert isinstance(configuration.timeout, int)


def test_cxsca_default_timeout_is_still_int(monkeypatch):
    _isolate_from_local_config_file(monkeypatch)
    monkeypatch.delenv("cxsca_timeout", raising=False)
    monkeypatch.delenv("CXSCA_TIMEOUT", raising=False)
    configuration = cxsca_construct_configuration()
    assert configuration.timeout == 60
    assert isinstance(configuration.timeout, int)
