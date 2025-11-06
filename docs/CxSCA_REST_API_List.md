# The CxSCA REST API List
1. Projects
    - get_all_projects
    - create_a_new_project
    - get_project_id_by_name
    - get_project_by_id
    - update_project
    - delete_project

2. Scans
    - get_all_scans_associated_with_a_project
    - get_latest_scan_id_of_a_project
    - get_scan_by_id
    - get_scan_status
    - get_scan_settings
    
3. Risk Reports
    - get_risk_report_summary
    - get_packages_of_a_scan
    - get_vulnerabilities_of_a_scan
    - get_licenses_of_a_scan
    - get_warnings_of_a_scan
    - ignore_a_vulnerability_for_a_specific_package_and_project
    - undo_the_ignore_state_of_an_ignored_vulnerability
    - get_scan_reports

4. Settings    
    - get_settings_for_a_specific_project
    - update_settings_for_a_specific_project
    
5. Scan Upload
    - generate_upload_link_for_scanning
    - upload_zip_content_for_scanning
    - scan_previously_uploaded_zip

AccessControlAPI