from CheckmarxPythonSDK.CxOne import (
    get_list_of_the_existing_query_repos,
    get_sast_queries_presets,
    get_sast_query_description,
    get_mapping_between_ast_and_sast_query_ids,
    get_sast_queries_preset_for_a_specific_scan,
    get_sast_queries_categories,
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


def test_get_mapping_between_ast_and_sast_query_ids():
    result = get_mapping_between_ast_and_sast_query_ids()
    assert result is not None


def test_get_sast_queries_preset_for_a_specific_scan():
    result = get_sast_queries_preset_for_a_specific_scan(scan_id="09ad7faf-74e5-415b-b81a-f4f209b736a4")
    assert result is not None


def test_get_sast_queries_categories():
    result = get_sast_queries_categories()
    assert result is not None
