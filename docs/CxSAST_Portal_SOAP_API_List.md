# The CxSAST Portal SOAP API List

## Portal Web Service (`CxPortalWebService`)

WSDL: `/CxWebInterface/Portal/CxWebService.asmx?wsdl`

| Python Class | Method | Description |
|---|---|---|
| CxPortalWebService | `add_license_expiration_notification` | Add license expiration notification |
| CxPortalWebService | `cancel_scan` | Cancel a running scan |
| CxPortalWebService | `cancel_scan_report` | Cancel a scan report generation |
| CxPortalWebService | `count_lines` | Count lines of source code |
| CxPortalWebService | `create_new_preset` | Create a new preset |
| CxPortalWebService | `create_scan_report` | Create a scan report (PDF/RTF/CSV/XML) |
| CxPortalWebService | `delete_preset` | Delete a preset |
| CxPortalWebService | `delete_project` | Delete a project |
| CxPortalWebService | `delete_projects` | Delete multiple projects |
| CxPortalWebService | `delete_scan` | Delete a scan |
| CxPortalWebService | `delete_scans` | Delete multiple scans |
| CxPortalWebService | `export_preset` | Export a preset |
| CxPortalWebService | `export_queries` | Export queries |
| CxPortalWebService | `get_associated_group_list` | Get associated group/team list |
| CxPortalWebService | `get_child_nodes` | Get child nodes in team hierarchy |
| CxPortalWebService | `get_compare_scan_results` | Compare results between two scans |
| CxPortalWebService | `get_configuration_set_list` | Get configuration set list |
| CxPortalWebService | `get_custom_field_values` | Get custom field values for a project/scan |
| CxPortalWebService | `get_custom_fields` | Get all custom fields |
| CxPortalWebService | `get_cx_description_by_query_id` | Get cached Cx description by query ID |
| CxPortalWebService | `get_cwe_description` | Get CWE description by CWE ID |
| CxPortalWebService | `get_executable_list` | Get list of executables |
| CxPortalWebService | `get_file_names_for_path` | Get file names for a result path |
| CxPortalWebService | `get_import_queries_status` | Get import queries status |
| CxPortalWebService | `get_name_of_user_who_marked_false_positive_from_comments_history` | Extract false-positive marker name from comments |
| CxPortalWebService | `get_path_comments_history` | Get path comments history |
| CxPortalWebService | `get_pivot_data` | Get pivot data for dashboard |
| CxPortalWebService | `get_preset_details` | Get preset details by ID |
| CxPortalWebService | `get_preset_list` | Get list of all presets |
| CxPortalWebService | `get_projects_display_data` | Get projects display data |
| CxPortalWebService | `get_projects_with_scans` | Get projects that have scans |
| CxPortalWebService | `get_queries_categories` | Get query categories |
| CxPortalWebService | `get_queries_for_scan` | Get queries used in a scan |
| CxPortalWebService | `get_query_collection` | Get full query collection |
| CxPortalWebService | `get_query_collection_for_language` | Get query collection by project type |
| CxPortalWebService | `get_query_description` | Get query description by CWE ID |
| CxPortalWebService | `get_query_description_by_query_id` | Get query description by query ID |
| CxPortalWebService | `get_query_id_by_language_group_and_query_name` | Find query ID by language, group, and name |
| CxPortalWebService | `get_query_short_description` | Get short query description |
| CxPortalWebService | `get_result_path` | Get result path detail |
| CxPortalWebService | `get_result_paths_for_query` | Get result paths for a query |
| CxPortalWebService | `get_result_state_flags` | Get result state flags |
| CxPortalWebService | `get_result_state_list` | Get list of result states |
| CxPortalWebService | `get_result_summary` | Get result summary for a scan |
| CxPortalWebService | `get_results` | Get results for a scan |
| CxPortalWebService | `get_results_for_query` | Get results for a specific query |
| CxPortalWebService | `get_results_for_scan` | Get results for a scan |
| CxPortalWebService | `get_scan_logs` | Get scan logs |
| CxPortalWebService | `get_scan_properties` | Get scan properties |
| CxPortalWebService | `get_scan_report` | Get a generated scan report |
| CxPortalWebService | `get_scan_report_status` | Get scan report generation status |
| CxPortalWebService | `get_scan_summary` | Get scan summary |
| CxPortalWebService | `get_scans_display_data_for_all_projects` | Get scans display data for all projects |
| CxPortalWebService | `get_scans_statuses` | Get statuses of all scans |
| CxPortalWebService | `get_server_language_list` | Get server language list |
| CxPortalWebService | `get_server_license_basic` | Get basic server license info |
| CxPortalWebService | `get_server_license_data` | Get full server license data |
| CxPortalWebService | `get_server_license_data_extended` | Get extended server license data |
| CxPortalWebService | `get_server_license_summary` | Get server license summary |
| CxPortalWebService | `get_source_by_scan_id` | Get source by scan ID (deprecated in 9.x) |
| CxPortalWebService | `get_sources_by_scan_id` | Get sources by scan ID |
| CxPortalWebService | `get_status_of_single_scan` | Get status of a single scan |
| CxPortalWebService | `get_user_profile_data` | Get user profile data |
| CxPortalWebService | `get_version_number` | Get server version number |
| CxPortalWebService | `get_version_number_as_int` | Get server version number as integer |
| CxPortalWebService | `import_preset` | Import a preset from file |
| CxPortalWebService | `import_queries` | Import queries from file |
| CxPortalWebService | `is_alive` | Check if server is alive |
| CxPortalWebService | `is_private_cloud` | Check if private cloud |
| CxPortalWebService | `is_smtp_host_configured` | Check if SMTP host is configured |
| CxPortalWebService | `is_valid_preset_name` | Check if a preset name is valid |
| CxPortalWebService | `lock_scan` | Lock a scan |
| CxPortalWebService | `postpone_scan` | Postpone a queued scan |
| CxPortalWebService | `unlock_scan` | Unlock a scan |
| CxPortalWebService | `update_preset` | Update a preset |
| CxPortalWebService | `update_result_comment` | Update a result comment |
| CxPortalWebService | `update_result_state` | Update a result state |
| CxPortalWebService | `update_scan_comment` | Update a scan comment |

## Audit Web Service (`CxAuditWebService`)

WSDL: `/cxwebinterface/Audit/CxAuditWebService.asmx?wsdl`

| Python Class | Method | Description |
|---|---|---|
| CxAuditWebService | `get_files_extensions` | Get file extensions |
| CxAuditWebService | `get_source_code_for_scan` | Get source code zip for a scan |
| CxAuditWebService | `upload_queries` | Upload query groups |
| CxAuditWebService | `get_results` | Get results for a scan |
| CxAuditWebService | `get_result_summary` | Get result summary for a scan |
| CxAuditWebService | `get_result_state_list` | Get list of result states |
| CxAuditWebService | `update_result_state` | Update a result state |
| CxAuditWebService | `update_scan_comment` | Update a scan comment |
| CxAuditWebService | `get_project_scans` | Get scans for a project |
| CxAuditWebService | `get_projects_with_scans` | Get projects that have scans |
| CxAuditWebService | `get_query_collection` | Get full query collection |
| CxAuditWebService | `get_query_collection_for_language` | Get query collection by project type |
| CxAuditWebService | `get_query_description` | Get query description by CWE ID |
| CxAuditWebService | `get_query_description_by_query_id` | Get query description by query ID |
| CxAuditWebService | `get_queries_categories` | Get query categories |
| CxAuditWebService | `get_preset_details` | Get preset details by ID |
| CxAuditWebService | `get_preset_list` | Get list of all presets |
| CxAuditWebService | `get_path_comments_history` | Get path comments history |
| CxAuditWebService | `get_project_configuration` | Get project configuration |
| CxAuditWebService | `get_license_details` | Get license details |
| CxAuditWebService | `get_engine_configuration` | Get engine configuration |
| CxAuditWebService | `get_hierarchy_group_tree` | Get hierarchy group tree |
| CxAuditWebService | `get_ancestry_group_tree` | Get ancestry group tree |
| CxAuditWebService | `keep_alive` | Keep audit session alive |
| CxAuditWebService | `import_queries` | Import queries from file |
| CxAuditWebService | `get_cache` | Get cache for a scan |
