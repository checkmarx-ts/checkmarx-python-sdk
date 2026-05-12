# encoding: utf-8

"""
    tests.test_engines_api

    :copyright Checkmarx
    :license MIT

"""

import pytest
from CheckmarxPythonSDK.CxRestAPISDK import EnginesAPI
from CheckmarxPythonSDK.CxRestAPISDK.sast.engines.dto import CxEngineDedication

_FAKE_ENGINE_NAME = "pytest_tmp_engine"
_FAKE_ENGINE_URI = "http://localhost:18089/"
_FAKE_ENGINE_IP = "localhost:18089"


def test_get_all_engine_server_details():
    engine_api = EnginesAPI()
    engine_server_details = engine_api.get_all_engine_server_details()
    assert engine_server_details is not None


def test_get_engine_id_by_name():
    engine_api = EnginesAPI()
    engines = engine_api.get_all_engine_server_details()
    assert engines is not None and len(engines) > 0
    engine_name = engines[0].name
    engine_id = engine_api.get_engine_id_by_name(engine_name)
    assert engine_id is not None


def test_register_engine():
    engine_api = EnginesAPI()
    engine_id = engine_api.get_engine_id_by_name(_FAKE_ENGINE_NAME)
    if engine_id:
        engine_api.unregister_engine_by_engine_id(engine_id)
    engine_server = engine_api.register_engine(
        _FAKE_ENGINE_NAME, _FAKE_ENGINE_URI, 0, 999999999, False,
        max_scans=1, dedications=None,
    )
    assert engine_server is not None


def test_get_engine_details():
    engine_api = EnginesAPI()
    engine_id = engine_api.get_engine_id_by_name(_FAKE_ENGINE_NAME)
    if engine_id is None:
        pytest.skip("Fake engine not registered")
    engine_detail = engine_api.get_engine_details(engine_id)
    assert engine_detail is not None


def test_update_engine_server():
    engine_api = EnginesAPI()
    engine_id = engine_api.get_engine_id_by_name(_FAKE_ENGINE_NAME)
    if engine_id is None:
        pytest.skip("Fake engine not registered")
    engine_server = engine_api.update_engine_server(
        engine_id, _FAKE_ENGINE_NAME,
        f"http://{_FAKE_ENGINE_IP}/d",
        0, 999999999, False, max_scans=1, dedications=None,
    )
    assert engine_server.id > 1


def test_update_an_engine_server_by_edit_single_field():
    engine_api = EnginesAPI()
    engine_id = engine_api.get_engine_id_by_name(_FAKE_ENGINE_NAME)
    if engine_id is None:
        pytest.skip("Fake engine not registered")
    is_successful = engine_api.update_an_engine_server_by_edit_single_field(
        engine_id, _FAKE_ENGINE_NAME,
        f"http://{_FAKE_ENGINE_IP}/d",
        0, 999999999, False, max_scans=1, dedications=None,
    )
    assert is_successful is True


def test_get_all_engine_configurations():
    engine_api = EnginesAPI()
    engine_configurations = engine_api.get_all_engine_configurations()
    assert engine_configurations is not None


def test_get_engine_configuration_id_by_name():
    name = "Default Configuration"
    engine_api = EnginesAPI()
    configuration_id = engine_api.get_engine_configuration_id_by_name(name)
    assert configuration_id is not None


def test_get_engine_configuration_by_id():
    name = "Default Configuration"
    engine_api = EnginesAPI()
    configuration_id = engine_api.get_engine_configuration_id_by_name(name)
    configuration = engine_api.get_engine_configuration_by_id(configuration_id)
    assert configuration is not None


def test_unregister_engine_by_engine_id():
    engine_api = EnginesAPI()
    engine_id = engine_api.get_engine_id_by_name(_FAKE_ENGINE_NAME)
    if engine_id is None:
        pytest.skip("Fake engine not registered")
    result = engine_api.unregister_engine_by_engine_id(engine_id)
    assert result is True
