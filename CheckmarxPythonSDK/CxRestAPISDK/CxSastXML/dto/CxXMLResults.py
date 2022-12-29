from .Query import Query


class CxXMLResults:
    def __init__(self, initiator_name, owner, scan_id, project_id, project_name, team_full_path_on_report_date,
                 deep_link, scan_start, preset, scan_time, lines_of_code_scanned, files_scanned, report_creation_time,
                 team, checkmarx_version, scan_comments, scan_type, source_origin, visibility, queries=None):
        """

        Args:
            initiator_name (str):
            owner (str):
            scan_id (int):
            project_id (int):
            project_name (str):
            team_full_path_on_report_date (str):
            deep_link (str):
            scan_start (str):
            preset (str):
            scan_time (str):
            lines_of_code_scanned (int):
            files_scanned (int):
            report_creation_time (str):
            team (str):
            checkmarx_version (str):
            scan_comments (str):
            scan_type (str):
            source_origin (str):
            visibility (str):
            queries (list of Query):
        """
        self.InitiatorName = initiator_name
        self.Owner = owner
        self.ScanId = scan_id
        self.ProjectId = project_id
        self.ProjectName = project_name
        self.TeamFullPathOnReportDate = team_full_path_on_report_date
        self.DeepLink = deep_link
        self.ScanStart = scan_start
        self.Preset = preset
        self.ScanTime = scan_time
        self.LinesOfCodeScanned = lines_of_code_scanned
        self.FilesScanned = files_scanned
        self.ReportCreationTime = report_creation_time
        self.Team = team
        self.CheckmarxVersion = checkmarx_version
        self.ScanComments = scan_comments
        self.ScanType = scan_type
        self.SourceOrigin = source_origin
        self.Visibility = visibility
        self.Queries = queries

    def __str__(self):
        return "CxXMLResults(initiator_name={initiator_name}, owner={owner}, scan_id={scan_id}, "\
               "project_id={project_id}, project_name={project_name}, "\
               "team_full_path_on_report_date={team_full_path_on_report_date}, deep_link={deep_link}, "\
               "scan_start={scan_start}, preset={preset}, scan_time={scan_time}, "\
               "lines_of_code_scanned={lines_of_code_scanned}, files_scanned={files_scanned}, "\
               "report_creation_time={report_creation_time}, team={team}, checkmarx_version={checkmarx_version}, "\
               "scan_comments={scan_comments}, scan_type={scan_type}, source_origin={source_origin}, "\
               "visibility={visibility}, queries={queries})".format(
                    initiator_name=self.InitiatorName,
                    owner=self.Owner,
                    scan_id=self.ScanId,
                    project_id=self.ProjectId,
                    project_name=self.ProjectName,
                    team_full_path_on_report_date=self.TeamFullPathOnReportDate,
                    deep_link=self.DeepLink,
                    scan_start=self.ScanStart,
                    preset=self.Preset,
                    scan_time=self.ScanTime,
                    lines_of_code_scanned=self.LinesOfCodeScanned,
                    files_scanned=self.FilesScanned,
                    report_creation_time=self.ReportCreationTime,
                    team=self.Team,
                    checkmarx_version=self.CheckmarxVersion,
                    scan_comments=self.ScanComments,
                    scan_type=self.ScanType,
                    source_origin=self.SourceOrigin,
                    visibility=self.Visibility,
                    queries=self.Queries,
               )


def construct_cx_xml_results(item, queries=None):
    return CxXMLResults(
                initiator_name=item.get('InitiatorName'),
                owner=item.get('Owner'),
                scan_id=int(item.get('ScanId')),
                project_id=int(item.get('ProjectId')),
                project_name=item.get('ProjectName'),
                team_full_path_on_report_date=item.get('TeamFullPathOnReportDate'),
                deep_link=item.get('DeepLink'),
                scan_start=item.get('ScanStart'),
                preset=item.get('Preset'),
                scan_time=item.get('ScanTime'),
                lines_of_code_scanned=int(item.get('LinesOfCodeScanned')),
                files_scanned=int(item.get('FilesScanned')),
                report_creation_time=item.get('ReportCreationTime'),
                team=item.get('Team'),
                checkmarx_version=item.get('CheckmarxVersion'),
                scan_comments=item.get('ScanComments'),
                scan_type=item.get('ScanType'),
                source_origin=item.get('SourceOrigin'),
                visibility=item.get('Visibility'),
                queries=queries
            )
