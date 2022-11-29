from CheckmarxPythonSDK.CxOne import (
    get_all_queries,
    get_queries_metadata,
    get_query_source,
    update_query_source,
)


def test_get_all_queries():
    all_queries = get_all_queries()
    assert all_queries is not None


def test_get_queries_metadata():
    queries_metadata = get_queries_metadata()
    assert queries_metadata is not None
    # 'HttpStatusCode: 500', 'ErrorMessage: {"message":"Failed to get queries descriptor","type":"ERROR","code":707}'


def test_get_query_source():
    all_queries = get_all_queries()
    if not all_queries:
        return
    query = all_queries[0]
    level, path = query.level, query.path
    query_source = get_query_source(level, path)
    assert query_source is not None
    # 'HttpStatusCode: 403', 'ErrorMessage: forbidden\n'


def test_update_query_source():
    # update_query_source(level, workspace_query)
    pass
