# Checkmarx Python SDK
This is a Checkmarx Python SDK. By using this SDK, Checkmarx users will be able to do automatic scanning with CxSAST and CxOSA.

This SDK uses Python requests package to initiate HTTP requests to do related CxSAST and CxOSA scanning, and reports generation.

Started from CxSAST 9.0, Access Control REST API is available.


# REST API Official Documents
For more information about Checkmarx REST API, please refer to Checkmarx knowledge Center：  
CxSAST (REST) API Summary:   https://checkmarx.atlassian.net/wiki/spaces/KC/pages/131039271/CxSAST+REST+API  

CxOSA  (REST) API Summary:   https://checkmarx.atlassian.net/wiki/spaces/CCOD/pages/856653848/CxOSA+API+Guide     
  
Access Control (REST) API Summary: https://checkmarx.atlassian.net/wiki/spaces/KC/pages/1098645604/Access+Control+REST+API+Summary

# Notice
Please use Python3

# Quick Start
First, Download and unzip this repository or clone this repository to your local drive.  
```
$ git clone https://github.com/checkmarx-ts/checkmarx-python-sdk.git
```

Next, install the library
```
$ pip install CheckmarxPythonSDK
```

Next, set up configuration (in e.g. ~/.Checkmarx/config.ini, or C:\\Users\\Administrator\\.Checkmarx\\config.ini)
```buildoutcfg
[checkmarx]
base_url = http://localhost:80
username = ******
password = ******
grant_type = password
scope = sast_rest_api
client_id = resource_owner_client
client_secret = 014DF517-39D1-4453-B7B3-9930C563627C
url =  %(base_url)s/cxrestapi
scan_preset = Checkmarx Default
configuration = Default Configuration
team_full_name = /CxServer
max_try = 3
```

Or you can get configuration information by using environment variables "cxsast_base_url", "cxsast_username", "cxsast_password", "cxsast_grant_type", "cxsast_scope", "cxsast_client_id", "cxsast_client_secret" this will override the earlier one.

Or you can get configuration information by passing command line arguments "--cxsast_base_url", "--cxsast_username", "--cxsast_password", "--cxsast_grant_type", "--cxsast_scope", "--cxsast_client_id", "--cxsast_client_secret"
for example run `Python <your_script>.py --cxsast_base_url=http://localhost:80 --cxsast_username=**** --cxsast_password=****` this will override the earlier one.

If using both SAST REST API and access control REST API, please change `scope` in config.ini into `sast_rest_api access_control_api`

# Examples
 
 Example 1: Scan from local zip file:
```Shell
python <Path to checkmarx-python-sdk>/examples/scan_from_local_zip.py
``` 

Example 2: Scan from git:
```Shell
python <Path to checkmarx-python-sdk>/examples/scan_from_git.py
``` 

Example 3: OSA scan demo:
```Shell
python <Path to checkmarx-python-sdk>/examples/osa_scan_demo.py
``` 


# The CxSAST and CxOSA REST API list

1. For REST API, use Bear Token for authentication
    - auth_headers (This is a global variable that stored token)
2. TeamAPI
    - get_all_teams
    - get_team_id_by_team_full_name                                         **(provided by SDK)**
    - get_team_full_name_by_team_id                                         **(provided by SDK)**
3. ProjectsAPI
    - get_all_project_details
    - create_project_with_default_configuration
    - get_project_id_by_project_name_and_team_full_name                     **(provided by SDK)**
    - get_project_details_by_id
    - update_project_by_id
    - update_project_name_team_id
    - delete_project_by_id
    - create_project_if_not_exists_by_project_name_and_team_full_name       **(provided by SDK)**
    - delete_project_if_exists_by_project_name_and_team_full_name           **(provided by SDK)**
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
    - get_short_vulnerability_description_for_a_scan_result
    - register_scan_report
    - get_report_status_by_id
    - get_report_by_id
    - is_scanning_finished                                                      **(provided by SDK)**
    - is_report_generation_finished                                             **(provided by SDK)**
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
    - BadRequestError                                                          **(provided by SDK)**
    - NotFoundError                                                            **(provided by SDK)**
    - CxError                                                   **(provided by SDK)**
11. AccessControlAPI
    - get_all_assignable_users
    - get_all_authentication_providers
    - submit_first_admin_user
    - get_admin_user_exists_confirmation
    - get_all_ldap_role_mapping
    - update_ldap_role_mapping
    - delete_ldap_role_mapping
    - test_ldap_server_connection
    - get_user_entries_by_search_criteria
    - get_group_entries_by_search_criteria
    - get_all_ldap_servers
    - create_new_ldap_server
    - get_ldap_server_by_id
    - update_ldap_server
    - delete_ldap_server
    - get_ldap_team_mapping
    - update_ldap_team_mapping
    - delete_ldap_team_mapping
    - get_my_profile
    - update_my_profile
    - get_all_oidc_clients
    - create_new_oidc_client
    - get_oidc_client_by_id
    - update_an_oidc_client
    - delete_an_oidc_client
    - get_all_permissions
    - get_permission_by_id
    - get_all_roles
    - create_new_role
    - get_role_by_id
    - update_a_role
    - delete_a_role
    - get_all_saml_identity_providers
    - create_new_saml_identity_provider
    - get_saml_identity_provider_by_id
    - update_new_saml_identity_provider
    - delete_a_saml_identity_provider
    - get_saml_service_provider_metadata
    - get_saml_service_provider
    - update_a_saml_service_provider
    - get_all_service_providers
    - get_service_provider_by_id
    - get_all_smtp_settings
    - create_smtp_settings
    - get_smtp_settings_by_id
    - update_smtp_settings
    - delete_smtp_settings
    - test_smtp_connection
    - get_all_system_locales
    - get_members_by_team_id
    - update_members_by_team_id
    - add_a_user_to_a_team
    - delete_a_member_from_a_team
    - get_all_teams
    - get_team_id_by_full_name
    - create_new_team
    - get_team_by_id
    - update_a_team
    - delete_a_team
    - generate_a_new_token_signing_certificate
    - upload_a_new_token_signing_certificate
    - get_all_users
    - get_user_id_by_name
    - create_new_user
    - get_user_by_id
    - update_a_user
    - delete_a_user
    - migrate_existing_user
    - get_all_windows_domains
    - get_windows_domain_id_by_name
    - create_a_new_windows_domain
    - get_windows_domain_by_id
    - update_a_windows_domain
    - delete_a_windows_domain
    - get_windows_domain_user_entries_by_search_criteria

# The CxSAST Portal SOAP API list
1. cx portal web service
    - create_new_preset
    - delete_preset
    - delete_project
    - delete_projects
    - get_preset_list
    - get_server_license_data
    - get_server_license_summary
    - get_version_number