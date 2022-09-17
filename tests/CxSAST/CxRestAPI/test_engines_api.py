# encoding: utf-8

"""
    tests.test_engines_api

    :copyright Checkmarx
    :license MIT

"""

from CheckmarxPythonSDK.CxRestAPISDK import EnginesAPI

another_engine_ip = 'happyy-laptop:8089'


def test_get_all_engine_server_details():
    engine_api = EnginesAPI()
    engine_server_details = engine_api.get_all_engine_server_details()
    assert engine_server_details is not None


def test_get_engine_id_by_name():
    engine_name = "Localhost"
    engine_api = EnginesAPI()
    engine_id = engine_api.get_engine_id_by_name(engine_name)
    assert engine_id is not None


def test_register_engine():
    engine_api = EnginesAPI()
    name = "engine2"
    engine_id = engine_api.get_engine_id_by_name(name)
    if engine_id:
        engine_api.unregister_engine_by_engine_id(engine_id)
    uri = "http://{ip}".format(ip=another_engine_ip)
    min_loc = 0
    max_loc = 999999999
    is_blocked = False
    engine_server = engine_api.register_engine(name, uri, min_loc, max_loc, is_blocked, max_scans=1)
    assert engine_server is not None


def test_get_engine_details():
    engine_name = "Localhost"
    engine_api = EnginesAPI()
    engine_id = engine_api.get_engine_id_by_name(engine_name)
    engine_detail = engine_api.get_engine_details(engine_id)
    assert engine_detail is not None


def test_update_engine_server():
    engine_name = "engine2"
    engine_api = EnginesAPI()
    engine_id = engine_api.get_engine_id_by_name(engine_name)
    name = "engine2"
    uri = "http://{ip}/d".format(ip=another_engine_ip)
    min_loc = 0
    max_loc = 999999999
    is_blocked = False
    max_scans = 1
    engine_server = engine_api.update_engine_server(engine_id, name, uri, min_loc, max_loc, is_blocked,
                                                    max_scans=max_scans)
    assert engine_server.id > 1


def test_update_an_engine_server_by_edit_single_field():
    engine_name = "engine2"
    engine_api = EnginesAPI()
    engine_id = engine_api.get_engine_id_by_name(engine_name)
    name = "engine2"
    uri = "http://{ip}/d".format(ip=another_engine_ip)
    min_loc = 0
    max_loc = 999999999
    is_blocked = False
    max_scans = 1
    is_successful = engine_api.update_an_engine_server_by_edit_single_field(engine_id, name, uri, min_loc, max_loc,
                                                                            is_blocked, max_scans=max_scans)
    assert is_successful is True


def test_get_all_engine_configurations():
    engine_api = EnginesAPI()
    engine_configurations = engine_api.get_all_engine_configurations()
    assert engine_configurations is not None


def test_get_engine_configuration_id_by_name():
    name = 'Default Configuration'
    engine_api = EnginesAPI()
    configuration_id = engine_api.get_engine_configuration_id_by_name(name)
    assert configuration_id is not None


def test_get_engine_configuration_by_id():
    name = 'Default Configuration'
    engine_api = EnginesAPI()
    configuration_id = engine_api.get_engine_configuration_id_by_name(name)
    configuration = engine_api.get_engine_configuration_by_id(configuration_id)
    assert configuration is not None


def test_unregister_engine_by_engine_id():
    engine_name = "engine2"
    engine_api = EnginesAPI()
    engine_id = engine_api.get_engine_id_by_name(engine_name)
    result = engine_api.unregister_engine_by_engine_id(engine_id)
    assert result is True