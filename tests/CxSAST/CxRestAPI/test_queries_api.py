"""
    tests.test_projects_api

    :copyright Checkmarx
    :license GPL-3

"""
from CheckmarxPythonSDK.CxRestAPISDK import QueriesAPI


def test_get_the_full_description_of_the_query():
    query_api = QueriesAPI()
    query_id = 589
    query_description = query_api.get_the_full_description_of_the_query(query_id)
    assert query_description is not None


def test_get_query_id_and_query_version_code():
    query_api = QueriesAPI()
    query_id_and_version_code = query_api.get_query_id_and_query_version_code(
        language="Java", query_name="SQL_Injection", severity="High"
    )
    assert query_id_and_version_code is not None


def test_get_preset_detail():
    result = QueriesAPI().get_preset_detail(preset_id=36)
    assert result is not None
