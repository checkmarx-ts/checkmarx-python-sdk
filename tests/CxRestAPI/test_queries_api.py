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
