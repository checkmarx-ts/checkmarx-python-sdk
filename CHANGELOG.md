Changelog
All notable changes to this project will be documented in  this file.

0.0.1 - 2020-03-05
* First release

0.0.2 - 2020-03-10
* Refactor code to change URL related variables from class variable to local variable to fix some bugs

0.0.3 - 2020-03-12
* Fix bugs for optional parameters used in URL

0.0.4 - 2020-05-22
* Add a verify CA certificate option for each HTTP request, default to False

0.0.5 - 2020-06-25
* Fix OSA API URL optional parameters bug

0.0.6 - 2020-07-15
* Fix OSA API URL optional itemsPerPage bug

0.0.7 - 2020-08-06
* Add SAST REST API for Get Short Vulnerability Description for a Scan Result

0.0.8 - 2020-08-31
* Add support for get configuration information from environment variables and command line arguments
* Add Portal SOAP APIs: create_new_preset, delete_preset, delete_project, delete_projects, get_preset_list, get_server_license_data, get_server_license_summary

0.1.1 - 2020-11-15
* Add a few support for OData API

0.1.2 - 2020-11-15
* Change get_results_and_write_to_csv_file to use only last scan of a project, instead of iterate through every scan

0.1.4 - 2020-11-27
* Fix portal soap api with retry_when_unauthorized, when have invalid token
* Refactor OData API

0.1.5 - 2020-12-02
* Add get_path_comments_history for portal soap api
* Add TeamName, TeamId for get_results_and_write_to_csv_file

0.1.6 - 2021-01-06
* Add configuration API
* Refactor Projects API get_all_project_details, get_project_details_by_id to use API v2, add custom fields into project detail

0.1.8 - 2021-01-20
* Add support for CxSCA API
* Add example scripts, cxsca_scan.py

0.1.9 - 2021-01-20
* Fix missing section CxSCA if not provided
* Add support for report folder in config

0.2.0 - 2021-01-21
* Fix forbidden issue for access control

0.2.1 - 2021-01-25
* Fix config max_try issue
* Add 3 new REST API for scan results
* Add 1 portal soap api get_query_collection

0.2.2 - 2021-02-07
* Refactor false positive scan results statistics logic

0.2.3 - 2021-03-25
* Fix bug for API POST /sast/results/tickets
* Make SCA access control url configurable

0.2.4 - 2021-03-26
* Fix bug for API POST /sast/results/tickets

0.2.5 - 2021-04-22
* Add support for Portal SOAP API: import_preset, import_queries, get_import_queries_status
* Add support for Portal SOAP API: export_preset, export_queries, get_query_id_by_language_group_and_query_name
* Modify support for Portal SOAP API create_scan_report

0.2.6 - 2021-05-06
* Fix bug when reponse status code is UNAUTHORIZED

0.2.7 - 2021-05-13
* Add support for the UploadQueries operation (CxAudit SOAP API)

0.2.8 - 2021-05-20
* Add support for CustomTaskAPI get_custom_task_by_name
* Add support for ScansAPI create_new_scan_with_settings
* Add support for Portal SOAP API get_version_number_as_int
* Add support for ScansAPI update_scan_result_labels_fields, get_scan_result_labels_fields

0.2.9 - 2021-08-09
* Add support for QueriesAPI get_the_full_description_of_the_query
* Update support for OsaAPI  get_osa_scan_libraries
* Add support for ScansAPI get_scan_logs, get_basic_metrics_of_a_scan, 
* get_parsed_files_metrics_of_a_scan, get_failed_queries_metrics_of_a_scan, 
* get_failed_general_queries_metrics_of_a_scan, get_succeeded_general_queries_metrics_of_a_scan
* Add support for ProjectsAPI set_project_queue_setting, update_project_queue_setting

0.3.0 - 2021-08-12
* Change config.py to be compatible with python 2.7

0.3.2 - 2021-08-17
* Fix EnginesAPI register_engine

0.3.3 - 2021-08-19
* Add field origin for csv report

0.3.5 - 2021-09-30
* Add field LOC for csv report

0.3.7 - 2022-01-04
* Add field PathId, DirectLink for csv report

0.3.8 - 2022-01-13
* Fix TeamAPI get_team_id_by_team_full_name if using "CxServer\SP\Company"

0.3.9 - 2022-01-20
* Add roleMapping and teamMapping support for access control api

0.4.0 - 2022-01-27
* Add Portal Soap API get_results_for_scan

0.4.1 - 2022-01-28
* Add Portal SOAP API get_result_path

0.4.2 - 2022-02-08
* fix not did retry_when_unauthorized for sca api

0.4.3 - 2022-02-09
* Add method define_data_retention_by_rolling_date, define_data_retention_by_rolling_months for DataRetentionAPI

0.4.4 - 2022-02-09
* Add new dependency in setup.py

0.4.5 - 2022-02-28
* Add ODATA API get_results_for_a_specific_scan_id_with_similarity_ids

0.4.6 - 2022-03-18
* Add support for CxReporting API

0.4.7 - 2022-03-19
* Add get_config_info_from_config_json_file

0.4.8 - 2022-03-20
* Add CxReporting api get_report

0.4.9 - 2022-03-20
* Fix CxReporting data transfer object CreateReportDTO and FilterDTO

0.5.0 - 2022-03-21
* Fix the team_id parameter default to None issue

0.5.1 - 2022-03-23
* Fix config file issue

0.5.2 - 2022-05-01
* Will not complain about missing config files only if names are non-empty 

0.5.3 - 2022-06-16
* Add support for using keyring to get password from Windows Credential Manager

0.5.4 - 2022-06-17
* Update setup.py

0.5.5 - 2022-06-17
* Fix NoKeyringError when using Keyring with PyInstaller

0.5.6 - 2022-09-20
* Refactor code to remove duplicate http request logic

0.5.7 - 2022-09-23
* Add Portal SOAP API get_associated_group_list
* Add Portal SOAP API get_projects_display_data

0.5.8 - 2022-09-23
* export AccessControlAPI for sca

0.5.9 - 2022-10-09
* make change to ScansAPI, method get_last_scan_id_of_a_project

0.6.0 - 2022-10-25
* Fix Portal SOAP API get_query_collection to handle query group without queries

0.6.1 - 2022-12-01
* Add command line option --cx_debug true to enable debug mode. In debug mode, the process to load configuration and every http request will be printed in console
* Rename CxAST module to CxOne as required by Checkmarx Product Team
* Add Keycloak API dto types

0.6.2 - 2022-12-01
* add creation_date field to User class in AccessControl

0.6.3 - 2022-12-01
* add Portal SOAP API postpone_scan

0.6.4 - 2022-12-09
* Fix --cx_debug command line option issue

0.6.5 - 2022-12-10
* Fix --cx_debug command line option issue

0.6.6 - 2023-01-05
* Fix the get_user_entries_by_search_criteria AccessControl method. 

0.6.7 - 2023-01-09
* Add support for sast xml to sarif

0.6.8 - 2023-01-10
* Add SCA API get_scan_reports

0.6.9 - 2023-01-30
* Fix SCA API get_states_associated_with_a_project and get_comments_associated_with_a_project

0.7.0 - 2023-02-26
* Fix AccessControl API get_windows_domain_user_entries_by_search_criteria

0.7.1 - 2023-04-12
* Add support for get_server_license_data

0.7.2 - 2023-04-13
* Fix AccessControl API get_all_roles

0.7.3 - 2023-04-25
* Fix ScansAPI __construct_scan_queue_detail

0.7.4 - 2023-05-08
* Add CxOne scanConfigurationAPI

0.7.5 - 2023-05-08
* Fix version issue

0.7.6 - 2023-05-11
* Fix use of undefined variable

0.7.7 - 2023-07-13
* Add Portal SOAP API get_pivot_data which is used by Portal Data Analysis

0.7.8 - 2023-07-20
* Fix SCA Access Control API
* Add some CxOne API

0.7.9 - 2023-08-08
* Add Portal SOAP API get_query_description_by_query_id

0.8.0 - 2023-08-09
* Add ODATA API get_all_scan_ids_within_a_predefined_time_range_for_all_projects_in_a_team, get_number_of_results_for_a_specific_scan_id_with_result_state

0.8.1 - 2023-08-11
* Fix get_query_id_by_language_group_and_query_name
* Add get_cx_description_by_query_id

0.8.2 - 2023-09-21
* Fix SAST Rest API, ScansAPI create_new_scan_with_settings, use API version 4

0.8.3 - 2023-11-16
* Add SCA MoR endpoints

0.8.4 - 2023-11-28
* Fix CxSAST REST API ProjectsAPI get_project_id_by_project_name_and_team_full_name

0.8.5 - 2024-02-08
* Add new support for SCA API: create_sbom_report, get_sbom_report_creation_status, get_sbom_supported_file_formats, run_file_analysis, retrieve_analysis_result 
* CxOne API report API, scan configuration API

0.8.6 - 2024-04-18
* Fix CxReporting 415 issue
* Fix SCA APi get_artifact_info

0.8.7 - 2024-04-19
* Fix CxOne ProjectInput.py criticality tag

0.8.8 - 2024-06-14
* Update Projects API set_remote_source_setting_to_git

0.8.9 - 2024-07-14
* Add support for GeneralAPI get_result_states, create_result_state, update_result_state, delete_result_state

0.9.0 - 2024-07-14
* Add support for ProjectsAPI force_scan_on_no_code_changes

0.9.1 - 2024-07-17
* Add support for new APIs

0.9.2 - 2024-08-23
* Add support for CxOne APIs

0.9.3 - 2024-08-26
* CxOne refactor header user-agent

0.9.4 - 2024-08-26
* Add support for proxy

0.9.5 - 2024-08-26
* Fix update_header proxy issue

0.9.6 - 2024-09-03
* Fix type checking

0.9.7 - 2024-09-11
* Fix SARIF report
* Fix CxOne project create issue

0.9.8 - 2024-09-12
* Fix CxOne upload file ssl cert verify issue

0.9.9 - 2024-09-12
* Fix CxSAST Odata api proxy issue

1.0.0 - 2024-09-12
* Fix Sarif report rueId use queryName instead of queryId