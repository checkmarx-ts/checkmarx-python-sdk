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