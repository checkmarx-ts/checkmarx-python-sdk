"""
    tests.test_queries_api

    :copyright Checkmarx
    :license GPL-3

"""
import pytest
from CheckmarxPythonSDK.CxRestAPISDK import QueriesAPI, ProjectsAPI


def _get_query_id():
    preset_id = ProjectsAPI().get_preset_id_by_name("Checkmarx Default")
    details = QueriesAPI().get_preset_detail(preset_id=preset_id)
    return details[0].get("queryId") if details else None


def test_get_the_full_description_of_the_query():
    query_api = QueriesAPI()
    query_id = _get_query_id()
    assert query_id is not None
    query_description = query_api.get_the_full_description_of_the_query(query_id)
    assert query_description is not None


def test_get_query_id_and_query_version_code():
    query_api = QueriesAPI()
    try:
        result = query_api.get_query_id_and_query_version_code(
            language="Java", query_name="SQL_Injection", severity="High"
        )
        assert result is not None
    except ValueError as e:
        if "404" in str(e):
            pytest.skip("get_query_id_and_query_version_code not supported on this server version")
        raise


def test_get_preset_detail():
    preset_id = ProjectsAPI().get_preset_id_by_name("Checkmarx Default")
    assert preset_id is not None
    result = QueriesAPI().get_preset_detail(preset_id=preset_id)
    assert result is not None
