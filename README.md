# Cx-REST-API-SDK-Python
A Checkmarx REST API SDK written in Python.

## Notice
This SDK is a Python package. In order to add this package into PYTHONPATH, please download this package,
create a ".pth" file under Python lib\site-packages, and set the absolute file path of the package CxRestAPISDK.
For example, in lib\site-packages\Checkmarx.pth,
input a line: C:\Users\HappyY\Downloads\SourceCode\GitHub\Cx-REST-API-SDK-Python\src

## Change configuration
Change configuration in file CxRestAPISDK/config/config.ini as needed.
Set your own username, password, team_full_name, and so on.
If you want to put config.ini in another location, set your own config.ini file path for CxConfig constructor.

## Checkmarx REST API Document
https://checkmarx.atlassian.net/wiki/spaces/KC/pages/131039271/CxSAST+REST+API

## The API list

1. AuthenticationAPI
    - auth_headers (This is a class variable that stored token)

2. TeamAPI
    - get_all_teams
    - get_team_id_by_team_full_name                                         (provided by SDK)
    - get_team_full_name_by_team_id                                         (provided by SDK)

3. ProjectsAPI
    - get_all_project_details
    - create_project_with_default_configuration
    - get_project_id_by_project_name_and_team_full_name                     (provided by SDK)
    - get_project_details_by_id
    - update_project_by_id
    - update_project_name_team_id
    - delete_project_by_id
    - create_project_if_not_exists_by_project_name_and_team_full_name       (provided by SDK)
    - delete_project_if_exists_by_project_name_and_team_full_name           (provided by SDK)
    - create_branched_project
    - get_all_issue_tracking_systems
    - get_issue_tracking_system_id_by_name
    - get_issue_tracking_system_details_by_id
    - get_project_exclude_settings_by_project_id
    - set_project_exclude_settings_by_project_id
    - get_remote_source_settings_for_git_by_project_id
    - set_remote_source_setting_to_git
    - get_remote_source_settings_for_svn_by_project_id
    - set_remote_source_settings_to_svn
    - get_remote_source_settings_for_tfs_by_project_id
    - set_remote_source_settings_to_tfs
    - get_remote_source_settings_for_custom_by_project_id
    - set_remote_source_setting_for_custom_by_project_id
    - get_remote_source_settings_for_shared_by_project_id
    - set_remote_source_settings_to_shared
    - get_remote_source_settings_for_perforce_by_project_id
    - set_remote_source_settings_to_perforce
    - set_remote_source_setting_to_git_using_ssh
    - set_remote_source_setting_to_svn_using_ssh
    - upload_source_code_zip_file
    - set_data_retention_settings_by_project_id
    - set_issue_tracking_system_as_jira_by_id
    - get_all_preset_details
    - get_preset_id_by_name
    - get_preset_details_by_preset_id

4. CustomTasksAPI
    - get_all_custom_tasks
    - get_custom_task_id_by_name
    - get_custom_task_by_id

5. CustomFieldsAPI
    - get_all_custom_fields
    - get_custom_field_id_by_name

6. ScansAPI
    - get_all_scans_for_project
    - get_last_scan_id_of_a_project
    - create_new_scan
    - get_sast_scan_details_by_scan_id
    - add_or_update_a_comment_by_scan_id
    - delete_scan_by_scan_id
    - get_statistics_results_by_scan_id
    - get_scan_queue_details_by_scan_id
    - update_queued_scan_status_by_scan_id
    - get_all_scan_details_in_queue
    - get_scan_settings_by_project_id
    - define_sast_scan_settings
    - update_sast_scan_settings
    - define_sast_scan_scheduling_settings
    - assign_ticket_to_scan_results
    - publish_last_scan_results_to_management_and_orchestration_by_project_id
    - get_the_publish_last_scan_results_to_management_and_orchestration_status
    - register_scan_report
    - get_report_status_by_id
    - get_report_by_id
    - is_scanning_finished                                                          (provided by SDK)
    - is_report_generation_finished                                                 (provided by SDK)

7. DataRetentionAPI
    - stop_data_retention
    - define_data_retention_date_range
    - define_data_retention_by_number_of_scans
    - get_data_retention_request_status

8. EnginesAPI
    - get_all_engine_server_details
    - get_engine_id_by_name
    - register_engine
    - unregister_engine_by_engine_id
    - get_engine_details
    - update_engine_server
    - get_all_engine_configurations
    - get_engine_configuration_id_by_name
    - get_engine_configuration_by_id

9. OsaAPI
    - get_all_osa_scan_details_for_project
    - get_last_osa_scan_id_of_a_project
    - get_osa_scan_by_scan_id
    - create_an_osa_scan_request
    - get_all_osa_file_extensions
    - get_osa_licenses_by_id
    - get_osa_scan_libraries
    - get_osa_scan_vulnerabilities_by_id
    - get_first_vulnerability_id
    - get_osa_scan_vulnerability_comments_by_id
    - get_osa_scan_summary_report

10. possible Exceptions
    - BadRequestError
    - NotFoundError
    - UnknownHttpStatusError

## examples
1. scan_from_local_zip
2. scan_from_git