from CheckmarxPythonSDK.CxOne import (
    get_all_queries,
    create_new_query,
    get_all_queries_search,
    get_queries_metadata,
    get_query_source,
    delete_overridden_query,
    update_query_source,
    create_new_session,
    get_all_active_sessions_related_to_webaudit,
    get_session_details,
    delete_session_with_specific_id,
    heath_check_to_ensure_session_is_kept_alive,
    check_if_sast_engine_is_ready_to_use,
    check_the_status_of_some_scan_related_requests,
    detect_the_languages_of_the_project_to_scan,
    scan_the_project_using_sast_engine,
    compile_the_queries_of_the_scanned_project,
    execute_the_queries_of_the_scanned_project,
    cancel_the_queries_execution,
    get_the_logs_associated_to_the_audit_session,
    retrieve_gpt_history,
    delete_gpt_history,
    process_gpt_prompt_request,
)

from CheckmarxPythonSDK.CxOne.dto import (
    Queries,
    Query,
    QuerySearch,
    MethodInfo,
    MethodParameter,
    Metadata,
    QueryRequest,
    WorkspaceQuery,
    SessionRequest,
    SessionResponse,
    Sessions,
    Session,
    SastStatus,
    RequestStatusNotReady,
    RequestStatusDetectLanguages,
    AuditQuery,
    CompilationResponse,
    ExecutionResponse,
    GPTMessage
)

def test_get_all_queries():
    all_queries = get_all_queries()
    assert all_queries is not None


def test_create_new_query():
    query_request = QueryRequest(
        path="queries/Java/Java_Critical_Risk/Code_Injection/",
        name="Test_Open_Redirect",
        source="CxList redirect = Find_Redirects()",
        metadata=Metadata(Cwe=94, Severity=1, IsExecutable=True, CxDescriptionID=0)
    )
    result = create_new_query(request_body=query_request.to_dict())
    assert result is not None


def test_get_all_queries_search():
    result = get_all_queries_search(session_id="")
    assert result is not None


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


def test_delete_overridden_query():
    result = delete_overridden_query(level="", path="")
    assert result is not None

#
# def test_update_query_source():
#     result = update_query_source(request_body="", session_id: str, level: str)
#     assert result is not None
#
#
# def test_create_new_session():
#     result = create_new_session(request_body: SessionRequest)
#     assert result is not None
#
#
# def test_get_all_active_sessions_related_to_webaudit():
#     result = get_all_active_sessions_related_to_webaudit(project_id: str = None, scan_id: str = None)
#     assert result is not None
#
#
# def test_get_session_details():
#     result = get_session_details(id: str)
#     assert result is not None
#
#
# def test_delete_session_with_specific_id():
#     result = delete_session_with_specific_id(id: str)
#     assert result is not None
#
#
# def test_heath_check_to_ensure_session_is_kept_alive():
#     result = heath_check_to_ensure_session_is_kept_alive(id: str, request_body=None)
#     assert result is not None
#
#
# def test_check_if_sast_engine_is_ready_to_use():
#     result = check_if_sast_engine_is_ready_to_use(id: str)
#     assert result is not None
#
#
# def test_check_the_status_of_some_scan_related_requests():
#     result = check_the_status_of_some_scan_related_requests(type: int)
#     assert result is not None
#
#
# def test_detect_the_languages_of_the_project_to_scan():
#     result = detect_the_languages_of_the_project_to_scan(id: str)
#     assert result is not None
#
#
# def test_scan_the_project_using_sast_engine():
#     result = scan_the_project_using_sast_engine(id: str)
#     assert result is not None
#
#
# def test_compile_the_queries_of_the_scanned_project():
#     result = compile_the_queries_of_the_scanned_project(request_body: List[AuditQuery], id: str)
#     assert result is not None
#
#
# def test_execute_the_queries_of_the_scanned_project():
#     result = execute_the_queries_of_the_scanned_project(request_body: List[AuditQuery], id: str)
#     assert result is not None
#
#
# def test_cancel_the_queries_execution():
#     result = cancel_the_queries_execution(id: str)
#     assert result is not None
#
#
# def test_get_the_logs_associated_to_the_audit_session():
#     result = get_the_logs_associated_to_the_audit_session(id: str)
#     assert result is not None
#
#
# def test_retrieve_gpt_history():
#     result = retrieve_gpt_history(id: str)
#     assert result is not None
#
#
# def test_delete_gpt_history():
#     result = delete_gpt_history(id: str)
#     assert result is not None
#
#
# def test_process_gpt_prompt_request():
#     result = process_gpt_prompt_request(request_body: dict, id: str)
#     assert result is not None
