# The CxSAST OData API List

Base URL: `/Cxwebinterface/odata/v1/`

## Projects

| Python Class | Method | OData Query |
|---|---|---|
| ProjectsODataAPI | `get_top_n_projects_by_risk_score` | `Projects?$expand=LastScan&$orderby=LastScan/RiskScore desc&$top={n}` |
| ProjectsODataAPI | `get_top_n_projects_by_last_scan_duration` | `Projects?$expand=LastScan&$orderby=LastScan/ScanDuration desc&$top={n}` |
| ProjectsODataAPI | `get_all_projects_with_their_last_scan_and_the_high_vulnerabilities` | `Projects?$expand=LastScan($expand=Results($filter=Severity eq 'High'))` |
| ProjectsODataAPI | `get_projects_that_have_high_vulnerabilities_in_the_last_scan` | `Projects?$expand=LastScan($expand=Results)&$filter=LastScan/Results/any(r: r/Severity eq 'High')` |
| ProjectsODataAPI | `get_the_number_of_issues_vulnerabilities_within_a_predefined_time_range_for_all_projects_in_a_team` | `Projects?$filter=OwningTeamId eq {team_id}&$expand=Scans($expand=ResultSummary;$select=Id,ScanRequestedOn,ResultSummary;$filter=ScanRequestedOn gt {start} and ScanRequestedOn lt {end})` |
| ProjectsODataAPI | `get_count_of_the_projects_in_the_system` | `Projects/$count` |
| ProjectsODataAPI | `get_all_projects_with_a_custom_field_that_has_a_specific_value` | `Projects?$filter=CustomFields/any(f: f/FieldName eq '{name}' and f/FieldValue eq '{value}')` |
| ProjectsODataAPI | `get_all_projects_with_a_custom_field_as_well_as_the_custom_field_information` | `Projects?$expand=CustomFields&$filter=CustomFields/any(f: f/FieldName eq '{name}')` |
| ProjectsODataAPI | `get_presets_associated_with_each_project` | `Projects?$expand=Preset` |
| ProjectsODataAPI | `get_all_projects_that_are_set_up_with_a_non_standard_configuration` | `Projects?$filter=EngineConfigurationId gt 1` |
| ProjectsODataAPI | `get_all_projects_id_name` | `Projects?$select=Id,Name` |
| ProjectsODataAPI | `get_all_projects_id_name_and_team_id_name` | `Projects?$select=Id,Name,OwningTeamId&$expand=OwningTeam($select=FullName)` |
| ProjectsODataAPI | `get_all_scan_ids_within_a_predefined_time_range_for_all_projects_in_a_team` | `Projects?$select=Id,Name&$filter=OwningTeamId eq {team_id}&$expand=Scans($select=Id;$filter=ScanRequestedOn gt {start} and ScanRequestedOn lt {end};$orderby=Id)` |

## Results

| Python Class | Method | OData Query |
|---|---|---|
| ResultsODataAPI | `get_results_for_a_specific_scan_id` | `Scans({scan_id})/Results` |
| ResultsODataAPI | `get_the_query_that_was_run_for_a_particular_unique_scan_result` | `Results(Id={result_id},ScanId={scan_id})?$expand=Query($select=Name)` |
| ResultsODataAPI | `get_results_for_a_specific_scan_id_with_query_language_state` | `Scans({scan_id})/Results?$select=Id,ScanId,QueryId,SimilarityId,PathId&$expand=Query($select=Name;$expand=QueryGroup($select=Name,LanguageName)),State($select=Name),Scan($select=Origin,LOC)` |
| ResultsODataAPI | `get_results_group_by_query_id_and_add_count_json_format` | — (utility — groups results from `get_results_for_a_specific_scan_id_with_query_language_state`) |
| ResultsODataAPI | `get_results_for_a_specific_scan_id_with_similarity_ids` | `Scans({scan_id})/Results?$expand=Query($select=Name;$expand=QueryGroup($select=Name,LanguageName)),State($select=Name),Scan($select=Origin,LOC)&$filter=SimilarityId in (...)` |
| ResultsODataAPI | `get_number_of_results_for_a_specific_scan_id_with_result_state` | `Scans({scan_id})/Results?$select=Id&$filter=State/Id in ({states})` |
| ResultsODataAPI | `get_similarity_ids_of_a_scan` | `Scans({scan_id})/Results?$select=SimilarityId,PathId` |

## Scans

| Python Class | Method | OData Query |
|---|---|---|
| ScansODataAPI | `get_all_data_for_a_specific_scan_id` | `Scans({scan_id})` |
| ScansODataAPI | `get_number_of_loc_scanned_for_a_specific_scan` | `Scans({scan_id})?$select=LOC` |
| ScansODataAPI | `get_number_of_loc_scanned_for_all_scan` | `Scans?$select=LOC,Id` |
| ScansODataAPI | `get_last_scan_id_of_a_project` | `Projects({project_id})/Scans?$orderby=Id desc&$top=1&$select=Id` |
| ScansODataAPI | `get_last_scan_of_a_project` | `Projects({project_id})/Scans?$orderby=Id desc&$top=1` |
| ScansODataAPI | `get_last_full_scan_id_of_a_project` | `Projects({project_id})/Scans?$filter=IsIncremental eq false&$orderby=Id desc&$top=1&$select=Id` |
| ScansODataAPI | `get_last_full_scan_of_a_project` | `Projects({project_id})/Scans?$filter=IsIncremental eq false&$orderby=Id desc&$top=1` |
| ScansODataAPI | `get_all_scans_within_a_predefined_time_range_and_their_h_m_l_values_for_a_project` | `Projects({project_id})/Scans?$filter=ScanRequestedOn gt {start} and ScanRequestedOn lt {end}&$select=Id,ScanRequestedOn,High,Medium,Low&$orderby=ScanRequestedOn desc` |
| ScansODataAPI | `get_the_state_of_each_scan_result_since_a_specific_date_for_a_project` | `Scans?$filter=ProjectId eq {project_id} and ScanRequestedOn gt {start_date}&$expand=Results($expand=State;$select=Id,ScanId,StateId)` |
| ScansODataAPI | `get_all_scan_id_of_a_project` | `Projects({project_id})/Scans?$select=Id` |

## Utilities (module-level functions)

| Function | Description |
|---|---|
| `get_project_id_name_and_scan_id_list` | Composes `get_all_projects_id_name` + `get_all_scan_id_of_a_project` |
| `scan_results_group_by_query_id` | Groups results dict by QueryId (Python-only) |
| `get_all_results_with_count_for_each_project_json_format` | Composes `get_project_id_name_and_scan_id_list` + `get_results_group_by_query_id_and_add_count_json_format` |
| `merge_results_by_similarity_id` | Merges two result lists by SimilarityId (Python-only) |
| `get_result` | Compose: last scan → results with query/language/state for a project |
| `get_results_and_write_to_csv_file` | Writes scan results to CSV using `get_result` |
| `dump_last_scan_results_of_each_project_into_csv_file` | Writes raw last-scan results to CSV |
| `dump_last_scan_results_statistics_of_each_project_into_csv_file` | Writes aggregated last-scan statistics to CSV |
