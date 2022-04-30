from CheckmarxPythonSDK.CxAST import (
    get_list_of_the_existing_query_repos,
    get_sast_queries_presets,
    get_sast_query_description,
)


def test_get_list_of_the_existing_query_repos():
    queries = get_list_of_the_existing_query_repos()
    assert queries is not None
    # 'HttpStatusCode: 404', 'ErrorMessage: 404 page not found\n'


def test_get_sast_queries_presets():
    presets = get_sast_queries_presets()
    assert presets is not None


def test_get_sast_query_description():
    description = get_sast_query_description(ids=["9001657640014870111"])
    assert description is not None
