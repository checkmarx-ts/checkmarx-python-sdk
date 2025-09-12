from CheckmarxPythonSDK.CxOne import (
    create_new_audit_session,
    heath_check_to_ensure_audit_session_is_kept_alive,
    delete_audit_session_with_specific_id,
    get_the_logs_associated_to_the_audit_session,
    scan_the_audit_session_sources,
    create_or_override_query,
    get_all_queries,
    get_data_of_a_specified_query,
    delete_a_specified_custom_or_overridden_query,
    update_specified_query_metadata,
    update_multiple_query_sources,
    validate_the_queries_provided,
    execute_the_queries_on_the_audit_session_scanned_project,
    check_the_status_of_a_specified_request,
    cancel_the_specified_request_execution,
    get_all_results_data_summary_tree_for_all_the_session_runs,
    get_all_vulnerabilities_related_to_a_given_result,
    get_specified_vulnerability_data_such_as_attack_vector,
    get_specified_result_debug_messages,
    get_query_builder_history,
    delete_query_builder_gpt_history,
    process_query_builder_gpt_request,
)
from CheckmarxPythonSDK.CxOne.dto import (
    SessionRequest,
)

def test_create_new_audit_session():
    project_id = "f6ec7d66-83bb-4228-88d0-67d64b98250f"
    scan_id = "440e9ad4-37d3-44a1-9617-bd8b089cb2c3"
    upload_url = "https://eu.ast.checkmarx.net/storage/uploads.ireland.eu-west-1-602005780816/014c234f-01ad-4233-a89b-9ac6d4ce94c4/938887cc-bfeb-49f5-b56e-7cf13bf2e3fe?X-Amz-Algorithm=AWS4-HMAC-SHA256&X-Amz-Credential=ast%2F20240605%2Fus-east-1%2Fs3%2Faws4_request&X-Amz-Date=20240605T032834Z&X-Amz-Expires=86400&X-Amz-Signature=6223157ba272f2268efeef8a8a1460bb9fe29228900523a8b41a39bcce21ce71&X-Amz-SignedHeaders=host"
    session_request = SessionRequest(
        project_id=project_id,
        scan_id=scan_id,
        scanner="sast"
    )
    result = create_new_audit_session(request_body=session_request)
    assert result is not None


    def test_heath_check_to_ensure_audit_session_is_kept_alive():
        heath_check_to_ensure_audit_session_is_kept_alive

    def test_delete_audit_session_with_specific_id():
        delete_audit_session_with_specific_id

    def test_get_the_logs_associated_to_the_audit_session():
        get_the_logs_associated_to_the_audit_session

    def test_scan_the_audit_session_sources():
        scan_the_audit_session_sources

    def test_create_or_override_query():
        create_or_override_query

    def test_get_all_queries():
        get_all_queries

    def test_get_data_of_a_specified_query():
        get_data_of_a_specified_query

    def test_delete_a_specified_custom_or_overridden_query():
        delete_a_specified_custom_or_overridden_query

    def test_update_specified_query_metadata():
        update_specified_query_metadata

    def test_update_multiple_query_sources():
        update_multiple_query_sources

    def test_validate_the_queries_provided():
        validate_the_queries_provided

    def test_execute_the_queries_on_the_audit_session_scanned_project():
        execute_the_queries_on_the_audit_session_scanned_project

    def test_check_the_status_of_a_specified_request():
        check_the_status_of_a_specified_request

    def test_cancel_the_specified_request_execution():
        cancel_the_specified_request_execution

    def test_get_all_results_data_summary_tree_for_all_the_session_runs():
        get_all_results_data_summary_tree_for_all_the_session_runs

    def test_get_all_vulnerabilities_related_to_a_given_result():
        get_all_vulnerabilities_related_to_a_given_result

    def test_get_specified_vulnerability_data_such_as_attack_vector():
        get_specified_vulnerability_data_such_as_attack_vector


    def test_get_specified_result_debug_messages():
        get_specified_result_debug_messages


    def test_get_query_builder_history():
        get_query_builder_history


    def test_delete_query_builder_gpt_history():
        delete_query_builder_gpt_history

    def test_process_query_builder_gpt_request():
        process_query_builder_gpt_request