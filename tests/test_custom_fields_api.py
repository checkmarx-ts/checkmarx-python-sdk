# encoding: utf-8

"""
    tests.test_custom_fields_api

    :copyright Checkmarx
    :license MIT

"""

from CheckmarxPythonSDK.CxRestAPISDK.sast.projects.CustomFieldsAPI import CustomFieldsAPI


def test_get_all_custom_fields():
    custom_fields_api = CustomFieldsAPI()
    custom_fields = custom_fields_api.get_all_custom_fields()
    assert custom_fields is not None


def test_get_custom_field_id_by_name():
    custom_fields_api = CustomFieldsAPI()
    custom_field_name = "projectManager"
    custom_field_id = custom_fields_api.get_custom_field_id_by_name(custom_field_name)
    assert custom_field_id is not None
