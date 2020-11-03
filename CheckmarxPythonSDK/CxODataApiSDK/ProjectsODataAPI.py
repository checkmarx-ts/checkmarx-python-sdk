
class ProjectsODataAPI(object):

    def __init__(self):
        self.retry = 0

    def top_5_projects_by_risk_score(self):
        """
        Requested result: list the 5 Projects whose most recent scans yielded the highest Risk Score
        Query used for retrieving the data:
        http://localhost/Cxwebinterface/odata/v1/Projects?$expand=LastScan&$orderby=LastScan/RiskScore%20desc&$top=5

        Returns:

        """
        pass

    def top_5_projects_by_last_scan_duration(self):
        """
        Requested result: list the 5 Projects whose most recent scan had the longest duration
        Query used for retrieving the data:
        http://localhost/Cxwebinterface/odata/v1/Projects?$expand=LastScan&$orderby=LastScan/ScanDuration%20desc&$top=5

        Returns:

        """
        pass

    def all_projects_with_their_last_scan_and_the_high_vulnerabilities(self):
        """
        Requested result: list all projects, and for each project list the security issues (vulnerabilities) with
        a High severity degree found in the project's most recent scan.
        Query used for retrieving the data:
        http://localhost/Cxwebinterface/odata/v1/Projects?$expand=LastScan
        ($expand=Results($filter=Severity%20eq%20CxDataRepository.Severity%27High%27))

        Returns:

        """
        pass

    def only_projects_that_have_high_vulnerabilities_in_the_last_scan(self):
        """
        Requested result:list only projects that had vulnerabilities with a High severity degree found
        in their last scan
        Query used for retrieving the data:
        http://localhost/Cxwebinterface/odata/v1/Projects?$expand=LastScan($expand=Results)&
        $filter=LastScan/Results/any(r:%20r/Severity%20eq%20CxDataRepository.Severity%27High%27)

        Returns:

        """
        pass

    def for_all_projects_in_a_team_return_the_number_of_issues_vulnerabilities_within_a_predefined_time_range(self):
        """
        Requested result:list the number of recurrent/resolved/new issues (vulnerabilities) detected by scans made in
        all projects that were carried out in a team within a predefined time range. The sample query below refers to
        a time range between the 23/07/2015 and 23/08/2015.

        Query used for retrieving the data:
        http://localhost/Cxwebinterface/odata/v1/Projects?
        $filter=OwningTeamId%20eq%20%2700000000-1111-1111-b111-989c9070eb11%27&
        $expand=Scans($expand=ResultSummary;$select=Id,ScanRequestedOn,ResultSummary;
        $filter=ScanRequestedOn%20gt%202015-07-23%20and%20ScanRequestedOn%20lt%202015-08-23)
        Returns:

        """
        pass

    def retrieve_a_count_of_the_projects_in_the_system(self):
        """
        Query used for retrieving the data: http://localhost/Cxwebinterface/odata/v1/Projects/$count
        Returns:

        """

    def retrieve_all_projects_with_a_custom_field_that_has_a_specific_value(self):
        """
        Requested result: retrieve all projects that contain a custom filed (for example, ProjManager, indicating the
        project manager's name) with a specific value (for example, Joe).

        Query used for retrieving the data:
        http://localhost/Cxwebinterface/odata/v1/Projects?$filter=CustomFields/any
        (f: f/FieldName eq 'ProjManager' and f/FieldValue eq 'Joe')

        Returns:

        """

    def retrieve_all_projects_with_a_custom_field_as_well_as_the_custom_field_information(self):
        """
        Requested result: retrieve all projects that contain a custom field (for example, ProjManager, indicating the
        project manager's name), as well as the custom field's information.

        Query used for retrieving the data:
        http://localhost/cxwebinterface/odata/v1/Projects?$expand=CustomFields&$filter=CustomFields/any
        (f: f/FieldName eq 'Field1')

        Returns:

        """

    def retrieve_a_list_of_presets_associated_with_each_project(self):
        """
        Requested result: retrieves a list of presets associated with each project

        Query used for retrieving the data: http://localhost/Cxwebinterface/odata/v1/Projects?$expand=Preset

        Returns:

        """

    def retrieve_all_projects_that_are_set_up_with_a_non_standard_configuration(self):
        """
        Requested result: retrieve all projects that are set up with a non-standard configuration,
        such as “Multi-Lanaguage Scan (v8.4.2 and up)".

        Query used for retrieving the data:
        http://localhost/Cxwebinterface/odata/v1/Projects?$filter=EngineConfigurationId
        or http://localhost/Cxwebinterface/odata/v1/Projects?$filter=EngineConfigurationId%20gt%201

        Returns:

        """
