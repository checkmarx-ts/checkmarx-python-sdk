# encoding: utf-8
"""
Portal SOAP API
Only support 9.x version.
Start from 9.0, Portal SOAP API needs Bear Token for authentication
"""

from os.path import exists
from typing import List, Union
from CheckmarxPythonSDK.configuration import Configuration
from CheckmarxPythonSDK.CxPortalSoapApiSDK.config import construct_configuration
from .sudsClient import SudsClient


class CxPortalWebService(object):

    def __init__(self, configuration: Configuration = None):
        if configuration is None:
            configuration = construct_configuration()
            # configuration.is_sast_portal = True
        self.suds_client = SudsClient(
            relative_web_interface_url="/CxWebInterface/Portal/CxWebService.asmx?wsdl",
            configuration=configuration,
        )

    def add_license_expiration_notification(self) -> dict:
        response = self.suds_client.execute(
            "AddLicenseExpirationNotification", sessionID="0"
        )
        return {
            "IsSuccesfull": response["IsSuccesfull"],
            "ErrorMessage": getattr(response, "ErrorMessage", None),
        }

    def create_new_preset(self, query_ids: List[str], name: str) -> dict:
        """

        Args:
            query_ids (`list` of int):
            name (str):

        Returns:
            dict

            sample return:
            {
                'queryIds':  [
                        343
                ],
                'id': 110003,
                'name': 'ddd',
                'owningteam': 1,
                'isPublic': True,
                'owner': None,
                'isUserAllowToUpdate': True,
                'isUserAllowToDelete': True,
                'IsDuplicate': False
            }
        """
        factory = self.suds_client.factory
        query_id_list = factory.ArrayOfLong(query_ids)
        cx_preset_detail = factory.CxPresetDetails(
            queryIds=query_id_list,
            id=0,
            name=name,
            owningteam=1,
            isPublic=True,
            isUserAllowToUpdate=True,
            isUserAllowToDelete=True,
            IsDuplicate=False,
        )
        response = self.suds_client.execute(
            "CreateNewPreset", sessionId="0", presrt=cx_preset_detail
        )
        preset = getattr(response, "preset", None)
        return {
            "IsSuccesfull": response["IsSuccesfull"],
            "ErrorMessage": getattr(response, "ErrorMessage", None),
            "preset": (
                {
                    "queryIds": getattr(getattr(preset, "queryIds", None), "long", []),
                    "id": preset.id,
                    "name": preset.name,
                    "owningteam": preset.owningteam,
                    "isPublic": preset.isPublic,
                    "owner": getattr(preset, "owner", None),
                    "isUserAllowToUpdate": preset.isUserAllowToUpdate,
                    "isUserAllowToDelete": preset.isUserAllowToDelete,
                    "IsDuplicate": preset.IsDuplicate,
                }
                if preset
                else None
            ),
        }

    def create_scan_report(
        self,
        scan_id,
        report_type,
        queries_all=True,
        queries_ids=None,
        results_severity_all=True,
        results_severity_criticl=True,
        results_severity_high=True,
        results_severity_medium=True,
        results_severity_low=True,
        results_severity_info=False,
        results_state_all=True,
        results_state_ids=None,
        display_categories_all=True,
        display_categories_ids=None,
        results_assigned_to_all=True,
        results_assigned_to_ids=None,
        results_assigned_to_usernames=None,
        results_per_vulnerability_all=True,
        results_per_vulnerability_maximum=50,
        header_options_link_to_online_results=True,
        header_options_team=True,
        header_options_checkmarx_version=True,
        header_options_comments=False,
        header_options_scan_custom_fields=True,
        header_options_scan_type=True,
        header_options_source_origin=True,
        header_options_density=True,
        general_options_only_executive_summary=False,
        general_options_table_of_contents=True,
        general_options_executive_summary=True,
        general_options_display_categories=True,
        general_options_display_language_hash_number=True,
        general_options_scanned_queries=False,
        general_options_scanned_files=False,
        general_options_vulnerabilities_description="Attached2Appendix",
        results_display_option_assigned_to=False,
        results_display_option_comments=False,
        results_display_option_link_to_online=True,
        results_display_option_result_description=True,
        results_display_option_snippets_mode="SourceAndDestination",
    ) -> dict:
        """

        Args:
            scan_id (int):
            report_type (str): 'PDF', 'RTF', 'CSV', 'XML'
            queries_all (bool):
            queries_ids (list, None):
            results_severity_all (bool):
            results_severity_high (bool):
            results_severity_medium (bool):
            results_severity_low (bool):
            results_severity_info (bool):
            results_state_all (bool):
            results_state_ids (list, None):
            display_categories_all (bool):
            display_categories_ids (list, None):
            results_assigned_to_all (bool):
            results_assigned_to_ids (list, None):
            results_assigned_to_usernames (list, None):
            results_per_vulnerability_all (bool):
            results_per_vulnerability_maximum (int):
            header_options_link_to_online_results (bool):
            header_options_team (bool):
            header_options_checkmarx_version (bool):
            header_options_comments (bool):
            header_options_scan_custom_fields (bool):
            header_options_scan_type (bool):
            header_options_source_origin (bool):
            header_options_density (bool):
            general_options_only_executive_summary (bool):
            general_options_table_of_contents (bool):
            general_options_executive_summary (bool):
            general_options_display_categories (bool):
            general_options_display_language_hash_number (bool):
            general_options_scanned_queries (bool):
            general_options_scanned_files (bool):
            general_options_vulnerabilities_description (str): "None", "Attached2Appendix", "Linked2Online"
            results_display_option_assigned_to (bool):
            results_display_option_comments (bool):
            results_display_option_link_to_online (bool):
            results_display_option_result_description (bool):
            results_display_option_snippets_mode (str): "None", "SourceAndDestination", "Full"

        Returns:

        """
        factory = self.suds_client.factory
        query_ids = factory.ArrayOfLong(queries_ids)
        queries = factory.CxWSQueriesFilter(All=queries_all, IDs=query_ids)

        results_severity = factory.CxWSResultsSeverityFilter(
            All=results_severity_all,
            Critical=results_severity_criticl,
            High=results_severity_high,
            Medium=results_severity_medium,
            Low=results_severity_low,
            Info=results_severity_info,
        )

        results_state_id_list = results_state_ids
        if results_state_id_list:
            results_state_id_list = factory.ArrayOfLong(results_state_id_list)
        results_state = factory.CxWSResultsStateFilter(
            All=results_state_all, IDs=results_state_id_list
        )

        display_categories_id_list = display_categories_ids
        if display_categories_id_list:
            display_categories_id_list = factory.ArrayOfLong(display_categories_id_list)
        display_categories = factory.CxWSDisplayCategoriesFilter(
            All=display_categories_all, IDs=display_categories_id_list
        )

        results_assigned_to_id_list = results_assigned_to_ids
        if results_assigned_to_id_list:
            results_assigned_to_id_list = factory.ArrayOfLong(
                results_assigned_to_id_list
            )
        results_assigned_to_username_list = results_assigned_to_usernames
        if results_assigned_to_username_list:
            results_assigned_to_username_list = factory.ArrayOfString(
                results_assigned_to_username_list
            )

        results_assigned_to = factory.CxWSResultsAssignedToFilter(
            All=results_assigned_to_all,
            IDs=results_assigned_to_id_list,
            Usernames=results_assigned_to_username_list,
        )

        results_per_vulnerability = factory.CxWSResultsPerVulnerabilityFilter(
            All=results_per_vulnerability_all,
            Maximimum=results_per_vulnerability_maximum,
        )

        version = self.get_version_number_as_int()

        if version < 940:
            header_options = factory.CxWSHeaderDisplayOptions(
                Link2OnlineResults=header_options_link_to_online_results,
                Team=header_options_team,
                CheckmarxVersion=header_options_checkmarx_version,
                ScanComments=header_options_comments,
                ScanType=header_options_scan_type,
                SourceOrigin=header_options_source_origin,
                ScanDensity=header_options_density,
            )
        else:
            header_options = factory.CxWSHeaderDisplayOptions(
                Link2OnlineResults=header_options_link_to_online_results,
                Team=header_options_team,
                CheckmarxVersion=header_options_checkmarx_version,
                ScanComments=header_options_comments,
                ScanCustomFields=header_options_scan_custom_fields,
                ScanType=header_options_scan_type,
                SourceOrigin=header_options_source_origin,
                ScanDensity=header_options_density,
            )

        general_option = factory.CxWSGeneralDisplayOptions(
            OnlyExecutiveSummary=general_options_only_executive_summary,
            TableOfContents=general_options_table_of_contents,
            ExecutiveSummary=general_options_executive_summary,
            DisplayCategories=general_options_display_categories,
            DisplayLanguageHashNumber=general_options_display_language_hash_number,
            ScannedQueries=general_options_scanned_queries,
            ScannedFiles=general_options_scanned_files,
            VulnerabilitiesDescription=general_options_vulnerabilities_description,
        )

        results_display_option = factory.CxWSResultDisplayOptions(
            AssignedTo=results_display_option_assigned_to,
            Comments=results_display_option_comments,
            Link2Online=results_display_option_link_to_online,
            ResultDescription=results_display_option_result_description,
            SnippetsMode=results_display_option_snippets_mode,
        )

        display_data = factory.CxWSReportDisplayData(
            Queries=queries,
            ResultsSeverity=results_severity,
            ResultsState=results_state,
            DisplayCategories=display_categories,
            ResultsAssigedTo=results_assigned_to,
            ResultsPerVulnerability=results_per_vulnerability,
            HeaderOptions=header_options,
            GeneralOption=general_option,
            ResultsDisplayOption=results_display_option,
        )
        filtered_report_request = factory.CxWSFilteredReportRequest(
            Type=report_type, ScanID=scan_id, DisplayData=display_data
        )
        response = self.suds_client.execute(
            "CreateScanReport", SessionID="0", Report=filtered_report_request
        )

        return {
            "IsSuccesfull": response["IsSuccesfull"],
            "ErrorMessage": getattr(response, "ErrorMessage", None),
            "ID": response["ID"],
        }

    def delete_preset(self, preset_id: int) -> dict:
        """

        Args:
            preset_id (int):

        Returns:

        """
        response = self.suds_client.execute("DeletePreset", sessionId="0", id=preset_id)
        return {
            "IsSuccesfull": response["IsSuccesfull"],
            "ErrorMessage": getattr(response, "ErrorMessage", None),
        }

    def delete_project(self, project_id: int) -> dict:
        """

        Args:
            project_id (int):

        Returns:

        """
        response = self.suds_client.execute(
            "DeleteProject", sessionID="0", projectID=project_id
        )
        return {
            "IsSuccesfull": response["IsSuccesfull"],
            "ErrorMessage": getattr(response, "ErrorMessage", None),
        }

    def delete_projects(self, project_ids: List[int], flag: str = "None") -> dict:
        """

        Args:
            project_ids (list of int):
            flag (str): "None", "RunningScans", "OnlyAllowedProjects"

        Returns:
           dict
        """
        factory = self.suds_client.factory
        cx_ws_request_delete_projects = factory.CxWSRequestDeleteProjects(
            SessionID="0",
            ProjectIDs=factory.ArrayOfLong(project_ids),
            Flags=factory.DeleteFlags([flag]),
        )
        response = self.suds_client.execute(
            "DeleteProjects", request=cx_ws_request_delete_projects
        )
        return {
            "IsSuccesfull": response["IsSuccesfull"],
            "ErrorMessage": getattr(response, "ErrorMessage", None),
            "Flags": response["Flags"],
            "IsConfirmation": response["IsConfirmation"],
            "NumOfDeletedProjects": response["NumOfDeletedProjects"],
            "UndeletedProjects": response["UndeletedProjects"],
        }

    def export_preset(self, preset_id: int) -> dict:
        """

        Args:
            preset_id (int):

        Returns:

        """
        response = self.suds_client.execute(
            "ExportPreset", sessionId="0", presetId=preset_id
        )
        return {
            "IsSuccesfull": response["IsSuccesfull"],
            "ErrorMessage": getattr(response, "ErrorMessage", None),
            "OverridenCorpQueryNames": getattr(response["OverridenCorpQueryNames"], "string", []),
            "Preset": response["Preset"],
        }

    def export_queries(self, queries_ids: List[int]) -> dict:
        """

        Args:
            queries_ids:

        Returns:

        """
        factory = self.suds_client.factory
        query_ids = factory.ArrayOfLong(queries_ids)
        response = self.suds_client.execute(
            "ExportQueries", sessionId="0", queryIds=query_ids
        )
        return {
            "IsSuccesfull": response["IsSuccesfull"],
            "ErrorMessage": getattr(response, "ErrorMessage", None),
            "Queries": getattr(response, "Queries", None),
        }

    def get_associated_group_list(self) -> dict:
        """

        Returns:
            {
                'IsSuccesfull': True,
                'ErrorMessage': None,
                'GroupList': [
                    {
                        'FullPath': '/CxServer',
                        'GroupName': 'CxServer',
                        'Guid': '1',
                        'ID': '1',
                        'Path': None,
                        'Type': 'Team'
                    }
                ]
            }
        """
        response = self.suds_client.execute("GetAssociatedGroupsList", SessionID="0")
        group_list = response.GroupList
        return {
            "IsSuccesfull": response["IsSuccesfull"],
            "ErrorMessage": getattr(response, "ErrorMessage", None),
            "GroupList": (
                [
                    {
                        "FullPath": item["FullPath"],
                        "GroupName": item["GroupName"],
                        "Guid": item["Guid"],
                        "ID": item["ID"],
                        "Path": getattr(item, "Path", None),
                        "Type": item["Type"],
                    }
                    for item in group_list.Group
                ]
                if group_list
                else None
            ),
        }

    def get_compare_scan_results(self, old_scan_id: int, new_scan_id: int) -> dict:
        """

        Args:
            old_scan_id (int):
            new_scan_id (int):

        Returns:

        """
        response = self.suds_client.execute(
            "GetCompareScanResults",
            sessionId="0",
            oldScanId=old_scan_id,
            newScanId=new_scan_id,
        )
        results_obj = getattr(response, "Results", None)
        items = (
            getattr(results_obj, "CxWSSingleResultCompareData", [])
            if results_obj is not None
            else []
        )
        return {
            "IsSuccesfull": response["IsSuccesfull"],
            "ErrorMessage": getattr(response, "ErrorMessage", None),
            "Results": [
                {
                    "QueryId": item.QueryId,
                    "PathId": item.PathId,
                    "SourceFolder": item.SourceFolder,
                    "SourceFile": item.SourceFile,
                    "SourceLine": item.SourceLine,
                    "SourceObject": item.SourceObject,
                    "DestFolder": item.DestFolder,
                    "DestFile": item.DestFile,
                    "DestLine": item.DestLine,
                    "NumberOfNodes": item.NumberOfNodes,
                    "DestObject": item.DestObject,
                    "Comment": item.Comment,
                    "State": item.State,
                    "Severity": item.Severity,
                    "AssignedUser": item.AssignedUser,
                    "ConfidenceLevel": item.ConfidenceLevel,
                    "ResultStatus": item.ResultStatus,
                    "IssueTicketID": item.IssueTicketID,
                    "QueryVersionCode": item.QueryVersionCode,
                    "ScanId": item.ScanId,
                    "ComparedToScanId": item.ComparedToScanId,
                    "ComparedToScanPathId": item.ComparedToScanPathId,
                    "QueryName": item.QueryName,
                }
                for item in items
            ],
        }

    def get_import_queries_status(self, request_id: int) -> dict:
        """

        Args:
            request_id (int):

        Returns:

        """
        response = self.suds_client.execute(
            "GetImportQueriesStatus", sessionId="0", requestId=request_id
        )
        return {
            "IsSuccesfull": response["IsSuccesfull"],
            "ErrorMessage": getattr(response, "ErrorMessage", None),
            "requestId": response["requestId"],
            "importQueryStatus": response["importQueryStatus"],
        }

    def get_path_comments_history(
        self, scan_id: int, path_id: int, label_type: str
    ) -> dict:
        """

        Args:
            scan_id (int):
            path_id (int):
            label_type (str):

        Returns:
            dict

            example:
            {
                'IsSuccesfull': True,
                'ErrorMessage': None,
                'Path': {
                    'SimilarityId': 0,
                    'PathId': 0,
                    'Comment': 'happy yang jvl_local, [2020年11月12日 16:57]: Changed status to Not Exploitable
                                happy yang jvl_local, [2020年11月12日 16:57]: Changed status to Proposed Not Exploitable ÿ',
                    'State': 0,
                    'Severity': 0,
                    'AssignedUser': None,
                    'Nodes': None
                }
            }
        """
        response = self.suds_client.execute(
            "GetPathCommentsHistory",
            sessionId="0",
            scanId=scan_id,
            pathId=path_id,
            labelType=label_type,
        )
        path = response.Path
        return {
            "IsSuccesfull": response["IsSuccesfull"],
            "ErrorMessage": getattr(response, "ErrorMessage", None),
            "Path": (
                {
                    "AssignedUser": getattr(path, "AssignedUser", None),
                    "Comment": getattr(path, "Comment", None),
                    "Nodes": getattr(path, "Nodes", None),
                    "PathId": path["PathId"],
                    "Severity": path["Severity"],
                    "SimilarityId": path["SimilarityId"],
                    "State": path["State"],
                }
                if path
                else None
            ),
        }

    def get_pivot_data(
        self,
        pivot_view_client_type: str,
        include_not_exploitable: bool = False,
        range_type: str = "PAST_MONTH",
        date_from: str = None,
        date_to: str = None,
    ) -> dict:
        """

        Args:
            pivot_view_client_type (str):  [AllProjectScans, LastMonthProjectScans, ProjectsLastScan, LastWeekOWASPTop10]
            include_not_exploitable (bool):
            range_type (str): [ALL, PAST_DAY, PAST_WEEK, PAST_MONTH, PAST_3_MONTH, PAST_YEAR, CUSTOM]
            date_from (str, optional): example: '2023-05-08-17-14-38'
            date_to (str, optional): example: '2023-10-08-17-14-38'

        Returns:

        """
        factory = self.suds_client.factory
        if pivot_view_client_type not in [
            "AllProjectScans",
            "LastMonthProjectScans",
            "ProjectsLastScan",
            "LastWeekOWASPTop10",
        ]:
            raise ValueError(
                "pivot_view_client_type should be AllProjectScans, LastMonthProjectScans, "
                "ProjectsLastScan, LastWeekOWASPTop10"
            )

        if range_type not in [
            "ALL",
            "PAST_DAY",
            "PAST_WEEK",
            "PAST_MONTH",
            "PAST_3_MONTH",
            "PAST_YEAR",
            "CUSTOM",
        ]:
            raise ValueError(
                "range_type should be ALL, PAST_DAY, PAST_WEEK, PAST_MONTH, PAST_3_MONTH, PAST_YEAR,"
                " CUSTOM"
            )
        not_exploitable = factory.PivotClientExploitabilityParam(
            IncludeNotExploitable=include_not_exploitable
        )
        from_date = None
        to_date = None
        if date_from:
            date_list = [int(item) for item in date_from.split("-")]
            from_date = factory.CxDateTime(
                Year=date_list[0],
                Month=date_list[1],
                Day=date_list[2],
                Hour=date_list[3],
                Minute=date_list[4],
                Second=date_list[5],
            )
        if date_to:
            date_list = [int(item) for item in date_to.split("-")]
            to_date = factory.CxDateTime(
                Year=date_list[0],
                Month=date_list[1],
                Day=date_list[2],
                Hour=date_list[3],
                Minute=date_list[4],
                Second=date_list[5],
            )
        date_range = factory.PivotClientDateRangeParam(
            RangeType=range_type, DateFrom=from_date, DateTo=to_date
        )
        array_of_pivot_client_base_param = factory.ArrayOfPivotClientBaseParam(
            [not_exploitable, date_range]
        )

        pivot_data_request = factory.CxPivotDataRequest(
            ViewName=pivot_view_client_type, Criteria=array_of_pivot_client_base_param
        )
        response = self.suds_client.execute(
            "GetPivotData", SessionID="0", PivotParams=pivot_data_request
        )
        return response

    def get_queries_categories(self) -> dict:
        """

        Returns:

        """
        response = self.suds_client.execute("GetQueriesCategories", sessionId="0")
        categories = response.QueriesCategories.CxQueryCategory
        return {
            "IsSuccesfull": response["IsSuccesfull"],
            "ErrorMessage": getattr(response, "ErrorMessage", None),
            "QueriesCategories": (
                [
                    {
                        "Id": category["Id"],
                        "CategoryName": category["CategoryName"],
                        "CategoryType": {
                            "Id": category["CategoryType"]["Id"],
                            "Name": category["CategoryType"]["Name"],
                            "Order": category["CategoryType"]["Order"],
                        },
                    }
                    for category in categories
                ]
                if categories
                else None
            ),
        }

    def get_query_collection(self) -> dict:
        response = self.suds_client.execute("GetQueryCollection", sessionId="0")
        query_groups = []
        for query_group in response.QueryGroups.CxWSQueryGroup:
            if query_group.Queries:
                queries = [
                    {
                        "Categories": (
                            [
                                {
                                    "CategoryName": category.CategoryName,
                                    "CategoryType": {
                                        "Id": category.CategoryType.Id,
                                        "Name": category.CategoryType.Name,
                                        "Order": category.CategoryType.Order,
                                    },
                                    "Id": category.Id,
                                }
                                for category in query.Categories.CxQueryCategory
                            ]
                            if query.Categories
                            else query.Categories
                        ),
                        "Cwe": query.Cwe,
                        "CxDescriptionID": query.CxDescriptionID,
                        "EngineMetadata": getattr(query, "EngineMetadata", None),
                        "IsEncrypted": query.IsEncrypted,
                        "IsExecutable": query.IsExecutable,
                        "Name": query.Name,
                        "PackageId": query.PackageId,
                        "QueryId": query.QueryId,
                        "QueryVersionCode": query.QueryVersionCode,
                        "Severity": query.Severity,
                        "Source": query.Source,
                        "Status": query.Status,
                        "Type": query.Type,
                    }
                    for query in query_group.Queries.CxWSQuery
                ]
            else:
                queries = []
            qg = {
                "Description": query_group.Description,
                "Impacts": getattr(query_group, "Impacts", None),
                "IsEncrypted": query_group.IsEncrypted,
                "IsReadOnly": query_group.IsReadOnly,
                "Language": query_group.Language,
                "LanguageName": query_group.LanguageName,
                "LanguageStateDate": query_group.LanguageStateDate,
                "LanguageStateHash": query_group.LanguageStateHash,
                "Name": query_group.Name,
                "OwningTeam": query_group.OwningTeam,
                "PackageFullName": query_group.PackageFullName,
                "PackageId": query_group.PackageId,
                "PackageType": query_group.PackageType,
                "PackageTypeName": query_group.PackageTypeName,
                "ProjectId": query_group.ProjectId,
                "Queries": queries,
                "Status": query_group.Status,
            }

            query_groups.append(qg)
        return {
            "IsSuccesfull": response.IsSuccesfull,
            "ErrorMessage": getattr(response, "ErrorMessage", None),
            "QueryGroups": query_groups,
        }

    @staticmethod
    def get_query_id_by_language_group_and_query_name(
        query_collections: List[dict],
        language: str,
        package_type_name: str,
        package_name: str,
        query_name: str,
    ) -> Union[int, None]:
        """

        Args:
            query_collections (list):
            language (str):
            package_type_name (str): ["Cx", "Corp"]
            package_name (str):
            query_name (str):

        Returns:
            int, None
        """
        query_id = None

        filtered_query_collections = [
            item
            for item in query_collections
            if item.get("LanguageName") == language
            and item.get("PackageTypeName") == package_type_name
            and item.get("Name") == package_name
        ]
        if len(filtered_query_collections) != 1:
            return query_id

        queries = filtered_query_collections[0].get("Queries")
        queries = [query for query in queries if query.get("Name") == query_name]
        if len(queries) == 1:
            query = queries[0]
            query_id = query.get("QueryId")
        return query_id

    def get_query_description_by_query_id(self, query_id: int) -> dict:
        """

        Args:
            query_id (int):

        Returns:
           dict
        """
        response = self.suds_client.execute(
            "GetQueryDescriptionByQueryId", sessionId="0", queryId=query_id
        )
        return {
            "IsSuccesfull": response.IsSuccesfull,
            "ErrorMessage": getattr(response, "ErrorMessage", None),
            "QueryDescription": response.QueryDescription,
        }

    def get_cx_description_by_query_id(self):
        query_description_dict = {}

        def get_query_description(query_id):
            """
            Args:
                query_id (int):
            Returns:
                 str
            """
            if query_id in query_description_dict.keys():
                query_description = query_description_dict.get(query_id)
            else:
                query_description = self.get_query_description_by_query_id(
                    query_id
                ).get("QueryDescription")
                query_description_dict.update({query_id: query_description})
            return query_description

        return get_query_description

    def get_name_of_user_who_marked_false_positive_from_comments_history(
        self, scan_id: int, path_id: int
    ) -> Union[str, None]:
        """

        Args:
            scan_id (int):
            path_id (int):

        Returns:
            first_and_last_name (str)
            example:
             "happy yang"
        """
        path_data = self.get_path_comments_history(scan_id, path_id, label_type="Remark").get("Path")
        comments_history = path_data.get("Comment") if path_data else None

        if not comments_history or "ÿ" not in comments_history:
            return None

        a_list = comments_history.split("ÿ")[0:-1]
        second_list = [
            item.split(",")[0] for item in a_list if "Not Exploitable" in item
        ]
        name_and_project = second_list[0]
        d_list = name_and_project.split(" ")
        e_list = d_list[0:2]
        return " ".join(e_list)

    def get_preset_list(self) -> dict:
        """

        Returns:
            dict
        """
        response = self.suds_client.execute("GetPresetList", SessionID="0")
        preset_list = response.PresetList
        return {
            "IsSuccesfull": response["IsSuccesfull"],
            "ErrorMessage": getattr(response, "ErrorMessage", None),
            "PresetList": (
                [
                    {
                        "PresetName": item["PresetName"],
                        "ID": item["ID"],
                        "owningUser": item["owningUser"],
                        "isUserAllowToUpdate": item["isUserAllowToUpdate"],
                        "isUserAllowToDelete": item["isUserAllowToDelete"],
                    }
                    for item in preset_list["Preset"]
                ]
                if preset_list
                else None
            ),
        }

    def get_projects_display_data(self) -> dict:
        """

        Returns:
        {
            "IsSuccesfull": True,
            "ErrorMessage": None,
            "ProjectList": [
                {
                    'Company': None,
                    'Group': 'CxServer',
                    'IsPublic': True,
                    'LastScanDate': {
                            'Hour': 10,
                            'Minute': 5,
                            'Second': 2,
                            'Day': 23,
                            'Month': 9,
                            'Year': 2022
                        },
                    'Owner': 'Admin',
                    'Permission': {
                        'IsAllowedToDelete': True,
                        'IsAllowedToDuplicate': True,
                        'IsAllowedToRun': True,
                        'IsAllowedToUpdate': True
                    },
                    'Preset': 'Checkmarx Default',
                    'ProjectName': 'jvl_git',
                    'ServiceProvider': None,
                    'TotalOsaScans': 0,
                    'TotalScans': 41,
                    'projectID': 5
                }
            ]
        """
        response = self.suds_client.execute("GetProjectsDisplayData", sessionID="0")
        project_list = response.projectList
        return {
            "IsSuccesfull": response["IsSuccesfull"],
            "ErrorMessage": getattr(response, "ErrorMessage", None),
            "ProjectList": (
                [
                    {
                        "Company": getattr(item, "Company", None),
                        "Group": item["Group"],
                        "IsPublic": item["IsPublic"],
                        "LastScanDate": item["LastScanDate"],
                        "Owner": item["Owner"],
                        "Permission": item["Permission"],
                        "Preset": item["Preset"],
                        "ProjectName": item["ProjectName"],
                        "ServiceProvider": getattr(item, "ServiceProvider", None),
                        "TotalOsaScans": item["TotalOsaScans"],
                        "TotalScans": item["TotalScans"],
                        "projectID": item["projectID"],
                    }
                    for item in project_list.ProjectDisplayData
                ]
                if project_list
                else None
            ),
        }

    def get_result_path(self, scan_id: int, path_id: int) -> dict:
        """

        Args:
            scan_id (int):
            path_id (int):

        Returns:

        """
        response = self.suds_client.execute(
            "GetResultPath", sessionId="0", scanId=scan_id, pathId=path_id
        )
        item = response.Path
        return {
            "IsSuccesfull": response["IsSuccesfull"],
            "ErrorMessage": getattr(response, "ErrorMessage", None),
            "Path": {
                "AssignedUser": item["AssignedUser"],
                "Comment": item["Comment"],
                "PathId": item["PathId"],
                "Severity": item["Severity"],
                "SimilarityId": item["SimilarityId"],
                "State": item["State"],
                "Nodes": [
                    {
                        "Column": node["Column"],
                        "DOM_Id": node["DOM_Id"],
                        "FileName": node["FileName"],
                        "FullName": node["FullName"],
                        "Length": node["Length"],
                        "Line": node["Line"],
                        "MethodLine": node["MethodLine"],
                        "Name": node["Name"],
                        "PathNodeId": node["PathNodeId"],
                    }
                    for node in item["Nodes"]["CxWSPathNode"]
                ],
            },
        }

    def get_results_for_scan(self, scan_id: int) -> dict:
        """

        Args:
            scan_id (int):

        Returns:

        """
        response = self.suds_client.execute(
            "GetResultsForScan", sessionID="0", scanId=scan_id
        )
        scan_results_list = response.Results.CxWSSingleResultData
        return {
            "IsSuccesfull": response["IsSuccesfull"],
            "ErrorMessage": getattr(response, "ErrorMessage", None),
            "ScanResults": (
                [
                    {
                        "QueryId": item["QueryId"],
                        "PathId": item["PathId"],
                        "SourceFolder": item["SourceFolder"],
                        "SourceFile": item["SourceFile"],
                        "SourceLine": item["SourceLine"],
                        "SourceObject": item["SourceObject"],
                        "DestFolder": item["DestFolder"],
                        "DestFile": item["DestFile"],
                        "DestLine": item["DestLine"],
                        "NumberOfNodes": item["NumberOfNodes"],
                        "DestObject": item["DestObject"],
                        "Comment": item["Comment"],
                        "State": item["State"],
                        "Severity": item["Severity"],
                        "AssignedUser": item["AssignedUser"],
                        "ConfidenceLevel": item["ConfidenceLevel"],
                        "ResultStatus": item["ResultStatus"],
                        "IssueTicketID": item["IssueTicketID"],
                        "QueryVersionCode": item["QueryVersionCode"],
                    }
                    for item in scan_results_list
                ]
                if scan_results_list
                else None
            ),
        }

    def get_server_license_data(self) -> dict:
        """

        Returns:

        """

        response = self.suds_client.execute("GetServerLicenseData", sessionID="0")
        supported_languages = response.SupportedLanguages
        return {
            "ExpirationDate": response["ExpirationDate"],
            "MaxConcurrentScans": response["MaxConcurrentScans"],
            "MaxLOC": response["MaxLOC"],
            "HID": response["HID"],
            "SupportedLanguages": (
                [
                    {"isSupported": item["isSupported"], "language": item["language"]}
                    for item in supported_languages["SupportedLanguage"]
                ]
                if supported_languages
                else None
            ),
            "MaxUsers": response["MaxUsers"],
            "CurrentUsers": response["CurrentUsers"],
            "MaxAuditUsers": response["MaxAuditUsers"],
            "CurrentAuditUsers": response["CurrentAuditUsers"],
            "IsOsaEnabled": response["IsOsaEnabled"],
            "OsaExpirationDate": response["OsaExpirationDate"],
            "Edition": response["Edition"],
            "ProjectsAllowed": response["ProjectsAllowed"],
            "CurrentProjectsCount": response["CurrentProjectsCount"],
        }

    def get_server_license_summary(self) -> dict:
        """

        Returns:

        """
        response = self.suds_client.execute("GetServerLicenseSummary", sessionID="0")
        supported_languages = response.SupportedLanguages
        return {
            "ExpirationDate": response["ExpirationDate"],
            "MaxConcurrentScans": response["MaxConcurrentScans"],
            "MaxLOC": response["MaxLOC"],
            "HID": response["HID"],
            "SupportedLanguages": (
                [
                    {"isSupported": item["isSupported"], "language": item["language"]}
                    for item in supported_languages["SupportedLanguage"]
                ]
                if supported_languages
                else None
            ),
            "MaxUsers": response["MaxUsers"],
            "CurrentUsers": response["CurrentUsers"],
            "MaxAuditUsers": response["MaxAuditUsers"],
            "CurrentAuditUsers": response["CurrentAuditUsers"],
            "IsOsaEnabled": response["IsOsaEnabled"],
            "OsaExpirationDate": response["OsaExpirationDate"],
            "Edition": response["Edition"],
            "ProjectsAllowed": response["ProjectsAllowed"],
            "CurrentProjectsCount": response["CurrentProjectsCount"],
        }

    def get_user_profile_data(self) -> dict:
        """
        Notice: This method is not implemented by Portal SOAP API.
        The response IsSuccesfull is always False

        Returns:

        """
        response = self.suds_client.execute("GetUserProfileData", sessionID="0")
        return {
            "IsSuccesfull": response["IsSuccesfull"],
            "ErrorMessage": getattr(response, "ErrorMessage", None),
            "ProfileData": getattr(response, "ProfileData", None),
        }

    def get_version_number(self) -> dict:
        """

        Returns:

        """
        response = self.suds_client.execute("GetVersionNumber")
        return {
            "IsSuccesfull": response["IsSuccesfull"],
            "ErrorMessage": getattr(response, "ErrorMessage", None),
            "Version": response["Version"],
        }

    def get_version_number_as_int(self) -> int:
        """
        8.9.0 -> 890
        9.2.0 -> 920
        9.3.0 -> 930
        9.4.0 -> 940
        9.4.1 -> 941
        Returns:
            int
        """
        version = self.get_version_number().get("Version").split(" ")[1]
        version = "".join(version.split("."))
        version = int(version)
        return version

    def import_preset(self, imported_file_path: str) -> Union[dict, None]:
        """

        Args:
            imported_file_path (str):

        Returns:

        """
        if not exists(imported_file_path):
            print("Error, the imported file {} not exist".format(imported_file_path))
            return

        with open(imported_file_path, "rb") as xml_file:
            imported_file = xml_file.read()
        response = self.suds_client.execute(
            "ImportPreset", sessionId="0", importedFile=imported_file
        )
        return {
            "IsSuccesfull": response["IsSuccesfull"],
            "ErrorMessage": getattr(response, "ErrorMessage", None),
            "requestId": response["requestId"],
            "importQueryStatus": response["importQueryStatus"],
        }

    def import_queries(self, imported_file_path: str) -> Union[dict, None]:
        """

        Args:
            imported_file_path (str):

        Returns:

        """
        if not exists(imported_file_path):
            print("Error, the imported file {} not exist".format(imported_file_path))
            return

        with open(imported_file_path, "rb") as xml_file:
            imported_file = xml_file.read()

        response = self.suds_client.execute(
            "ImportQueries", sessionId="0", importedFile=imported_file
        )
        return {
            "IsSuccesfull": response["IsSuccesfull"],
            "ErrorMessage": getattr(response, "ErrorMessage", None),
            "requestId": response["requestId"],
            "importQueryStatus": response["importQueryStatus"],
        }

    def lock_scan(self, scan_id: int) -> dict:
        """

        Args:
            scan_id (int):

        Returns:

        """
        response = self.suds_client.execute(
            "LockScan", i_SessionID="0", i_ScanID=scan_id
        )
        return {
            "IsSuccesfull": response["IsSuccesfull"],
            "ErrorMessage": getattr(response, "ErrorMessage", None),
        }

    def postpone_scan(self, scan_id: int) -> dict:
        """

        Args:
            scan_id (int):

        Returns:

        """
        response = self.suds_client.execute(
            "PostponeScan", sessionID="0", RunId=str(scan_id)
        )
        return {
            "IsSuccesfull": response["IsSuccesfull"],
            "ErrorMessage": getattr(response, "ErrorMessage", None),
        }

    def get_source_by_scan_id(self, scan_id: int, file_name: str) -> dict:
        """Retrieve source code for a specific file in a scan (deprecated).

        This SOAP operation is no longer supported in CxSAST 9.x. The server
        returns IsSuccesfull=False with "This action is no longer supported."
        Use :meth:`get_sources_by_scan_id` (plural) instead.

        Args:
            scan_id (int):
            file_name (str): the file path to retrieve source for

        Returns:
            dict: always IsSuccesfull=False on 9.x
        """
        response = self.suds_client.execute(
            "GetSourceByScanID",
            sessionID="0",
            scanID=str(scan_id),
            fileToRetreive=file_name,
        )
        return {
            "IsSuccesfull": response.IsSuccesfull,
            "ErrorMessage": getattr(response, "ErrorMessage", None),
            "source": getattr(response, "source", None),
        }

    def get_sources_by_scan_id(self, scan_id: int, file_names: list) -> dict:
        """Retrieve source code for specific files in a scan.

        Args:
            scan_id (int):
            file_names (list of str): file paths to retrieve source for

        Returns:
            dict::
                {
                    "IsSuccesfull": True,
                    "ErrorMessage": None,
                    "sources": [
                        {"IsSuccesfull": True, "Source": "<content>", "Encode": "Unicode (UTF-8)"},
                        ...
                    ],
                }
        """
        files_array = self.suds_client.factory.ArrayOfString(list(file_names))
        response = self.suds_client.execute(
            "GetSourcesByScanID",
            sessionID="0",
            scanID=str(scan_id),
            filesToRetreive=files_array,
        )
        content_list = getattr(
            response, "cxWSResponseSourcesContent", None
        )
        sources = []
        if content_list:
            items = getattr(content_list, "CxWSResponseSourceContent", None)
            if items is not None:
                if not isinstance(items, list):
                    items = [items]
                sources = [
                    {
                        "IsSuccesfull": item.IsSuccesfull,
                        "Source": item.Source,
                    }
                    for item in items
                ]
        return {
            "IsSuccesfull": response.IsSuccesfull,
            "ErrorMessage": getattr(response, "ErrorMessage", None),
            "Encode": getattr(response, "Encode", None),
            "sources": sources,
        }

    def get_file_names_for_path(self, scan_id: int, path_id: int) -> dict:
        """Get file names associated with a result path.

        Args:
            scan_id (int):
            path_id (int):

        Returns:
            dict::
                {
                    "IsSuccesfull": True,
                    "ErrorMessage": None,
                    "fileNames": ["\\\\path\\\\to\\\\file.jsp"],
                }
        """
        response = self.suds_client.execute(
            "GetFileNamesForPath",
            sessionId="0",
            scanId=scan_id,
            pathId=path_id,
        )
        fnames = getattr(response, "fileNames", None)
        file_names = []
        if fnames:
            strings = getattr(fnames, "string", None)
            if strings is not None:
                if not isinstance(strings, list):
                    strings = [strings]
                file_names = strings
        return {
            "IsSuccesfull": response.IsSuccesfull,
            "ErrorMessage": getattr(response, "ErrorMessage", None),
            "fileNames": file_names,
        }

    def unlock_scan(self, scan_id: int) -> dict:
        """

        Args:
            scan_id (int):

        Returns:

        """
        response = self.suds_client.execute(
            "UnlockScan", i_SessionID="0", i_ScanID=scan_id
        )
        return {
            "IsSuccesfull": response["IsSuccesfull"],
            "ErrorMessage": getattr(response, "ErrorMessage", None),
        }

    def get_preset_details(self, preset_id: int) -> dict:
        response = self.suds_client.execute(
            "GetPresetDetails", sessionId="0", id=preset_id
        )
        preset = getattr(response, "preset", None)
        return {
            "IsSuccesfull": response["IsSuccesfull"],
            "ErrorMessage": getattr(response, "ErrorMessage", None),
            "preset": (
                {
                    "queryIds": getattr(getattr(preset, "queryIds", None), "long", []),
                    "id": preset.id,
                    "name": preset.name,
                    "owningteam": preset.owningteam,
                    "isPublic": preset.isPublic,
                    "owner": getattr(preset, "owner", None),
                    "isUserAllowToUpdate": preset.isUserAllowToUpdate,
                    "isUserAllowToDelete": preset.isUserAllowToDelete,
                    "IsDuplicate": preset.IsDuplicate,
                }
                if preset
                else None
            ),
        }

    def update_preset(self, preset_id: int, query_ids: list, name: str) -> dict:
        factory = self.suds_client.factory
        query_id_list = factory.ArrayOfLong(query_ids)
        cx_preset_detail = factory.CxPresetDetails(
            queryIds=query_id_list,
            id=preset_id,
            name=name,
            owningteam=1,
            isPublic=True,
            isUserAllowToUpdate=True,
            isUserAllowToDelete=True,
            IsDuplicate=False,
        )
        response = self.suds_client.execute(
            "UpdatePreset", sessionId="0", presrt=cx_preset_detail
        )
        preset = getattr(response, "preset", None)
        return {
            "IsSuccesfull": response["IsSuccesfull"],
            "ErrorMessage": getattr(response, "ErrorMessage", None),
            "preset": (
                {
                    "queryIds": getattr(getattr(preset, "queryIds", None), "long", []),
                    "id": preset.id,
                    "name": preset.name,
                    "owningteam": preset.owningteam,
                    "isPublic": preset.isPublic,
                    "owner": getattr(preset, "owner", None),
                    "isUserAllowToUpdate": preset.isUserAllowToUpdate,
                    "isUserAllowToDelete": preset.isUserAllowToDelete,
                    "IsDuplicate": preset.IsDuplicate,
                }
                if preset
                else None
            ),
        }

    def get_result_state_list(self) -> dict:
        response = self.suds_client.execute("GetResultStateList", sessionID="0")
        result_state_list = getattr(
            response, "ResultStateList", None
        )
        items = getattr(result_state_list, "ResultState", []) if result_state_list else []
        return {
            "IsSuccesfull": response["IsSuccesfull"],
            "ErrorMessage": getattr(response, "ErrorMessage", None),
            "ResultStateList": [
                {
                    "ResultName": item.ResultName,
                    "ResultID": item.ResultID,
                    "ResultPermission": item.ResultPermission,
                }
                for item in (items if isinstance(items, list) else [items])
            ],
        }

    def get_scan_report(self, report_id: int) -> dict:
        response = self.suds_client.execute(
            "GetScanReport", SessionID="0", ReportID=report_id
        )
        return {
            "IsSuccesfull": response["IsSuccesfull"],
            "ErrorMessage": getattr(response, "ErrorMessage", None),
            "ScanResults": getattr(response, "ScanResults", None),
            "containsAllResults": response["containsAllResults"],
        }

    def get_scan_report_status(self, report_id: int) -> dict:
        response = self.suds_client.execute(
            "GetScanReportStatus", SessionID="0", ReportID=report_id
        )
        return {
            "IsSuccesfull": response["IsSuccesfull"],
            "ErrorMessage": getattr(response, "ErrorMessage", None),
            "Status": getattr(response, "Status", None),
        }

    def cancel_scan_report(self, report_id: int) -> dict:
        response = self.suds_client.execute(
            "CancelScanReport", SessionID="0", ReportID=report_id
        )
        return {
            "IsSuccesfull": response["IsSuccesfull"],
            "ErrorMessage": getattr(response, "ErrorMessage", None),
        }

    def get_results(self, scan_id: int) -> dict:
        response = self.suds_client.execute(
            "GetResults", sessionId="0", scanId=scan_id
        )
        result_collection = getattr(response, "ResultCollection", None)
        results = []
        if result_collection:
            query_groups = getattr(result_collection, "QueryGroups", None)
            if query_groups:
                groups = getattr(query_groups, "CxWSQueryGroup", [])
                if not isinstance(groups, list):
                    groups = [groups]
                for qg in groups:
                    for qr in (getattr(getattr(qg, "QueryResults", None), "CxWSQueryResult", []) or []):
                        if not isinstance(qr, list):
                            qr_list = [qr] if qr else []
                        else:
                            qr_list = qr
                        for item in qr_list:
                            results.append({
                                "QueryId": item.QueryId,
                                "QueryName": item.QueryName,
                                "QueryVersionCode": item.QueryVersionCode,
                                "QueryGroupName": getattr(item, "QueryGroupName", None),
                                "ResultPathList": getattr(item, "ResultPathList", None),
                            })
        return {
            "IsSuccesfull": response["IsSuccesfull"],
            "ErrorMessage": getattr(response, "ErrorMessage", None),
            "Results": results,
        }

    def get_result_summary(self, scan_id: int) -> dict:
        response = self.suds_client.execute(
            "GetResultSummary", sessionId="0", scanId=scan_id
        )
        return {
            "IsSuccesfull": response["IsSuccesfull"],
            "ErrorMessage": getattr(response, "ErrorMessage", None),
            "ResultSummary": getattr(response, "ResultSummary", None),
        }

    def get_query_collection_for_language(
        self, project_type: str = "Regular", project_id: int = 0
    ) -> dict:
        response = self.suds_client.execute(
            "GetQueryCollectionForLanguage",
            sessionId="0",
            projectType=project_type,
            projectId=project_id,
        )
        query_groups = []
        for query_group in response.QueryGroups.CxWSQueryGroup:
            queries = []
            if query_group.Queries:
                for query in query_group.Queries.CxWSQuery:
                    queries.append({
                        "QueryId": query.QueryId,
                        "Name": query.Name,
                        "Severity": query.Severity,
                        "Status": query.Status,
                        "Cwe": query.Cwe,
                        "Source": query.Source,
                        "IsExecutable": query.IsExecutable,
                        "QueryVersionCode": query.QueryVersionCode,
                        "Type": query.Type,
                        "CxDescriptionID": query.CxDescriptionID,
                    })
            query_groups.append({
                "Name": query_group.Name,
                "Language": query_group.Language,
                "LanguageName": query_group.LanguageName,
                "PackageTypeName": query_group.PackageTypeName,
                "PackageId": query_group.PackageId,
                "Queries": queries,
            })
        return {
            "IsSuccesfull": response.IsSuccesfull,
            "ErrorMessage": getattr(response, "ErrorMessage", None),
            "QueryGroups": query_groups,
        }

    def get_query_description(self, cwe_id: int) -> dict:
        response = self.suds_client.execute(
            "GetQueryDescription", sessionId="0", cweID=cwe_id
        )
        return {
            "IsSuccesfull": response["IsSuccesfull"],
            "ErrorMessage": getattr(response, "ErrorMessage", None),
            "QueryDescription": getattr(response, "QueryDescription", None),
        }

    def get_query_short_description(self, query_id: int) -> dict:
        response = self.suds_client.execute(
            "GetQueryShortDescription", sessionId="0", queryId=query_id
        )
        return {
            "IsSuccesfull": response["IsSuccesfull"],
            "ErrorMessage": getattr(response, "ErrorMessage", None),
            "QueryShortDescription": getattr(response, "QueryShortDescription", None),
        }

    def get_scans_display_data_for_all_projects(self) -> dict:
        response = self.suds_client.execute(
            "GetScansDisplayDataForAllProjects", sessionID="0"
        )
        scans_list = getattr(response, "ScansDisplayData", None)
        items = (
            getattr(scans_list, "ScanDisplayData", [])
            if scans_list
            else []
        )
        return {
            "IsSuccesfull": response["IsSuccesfull"],
            "ErrorMessage": getattr(response, "ErrorMessage", None),
            "ScansDisplayData": [
                {
                    "ScanID": item.ScanID,
                    "ProjectID": item.ProjectID,
                    "ProjectName": item.ProjectName,
                    "TeamName": item.TeamName,
                    "ScanStartDate": getattr(item, "ScanStartDate", None),
                    "ScanFinishDate": getattr(item, "ScanFinishDate", None),
                    "ScanStatus": getattr(item, "ScanStatus", None),
                    "ScanType": getattr(item, "ScanType", None),
                    "TotalResults": item.TotalResults,
                    "HighResults": item.HighResults,
                    "MediumResults": item.MediumResults,
                    "LowResults": item.LowResults,
                    "InfoResults": item.InfoResults,
                    "IsLocked": item.IsLocked,
                }
                for item in (items if isinstance(items, list) else [items])
            ],
        }

    def get_scan_summary(self, scan_id: int) -> dict:
        response = self.suds_client.execute(
            "GetScanSummary", i_SessionID="0", i_ScanID=scan_id, auditEvent=False
        )
        return {
            "IsSuccesfull": response["IsSuccesfull"],
            "ErrorMessage": getattr(response, "ErrorMessage", None),
            "ScanSummary": getattr(response, "ScanSummary", None),
            "Partial": getattr(response, "Partial", None),
        }

    def get_server_license_basic(self) -> dict:
        response = self.suds_client.execute("GetServerLicenseBasic", sessionID="0")
        return {
            "IsSuccesfull": response["IsSuccesfull"],
            "ErrorMessage": getattr(response, "ErrorMessage", None),
            "LicenseExpirationDate": getattr(response, "LicenseExpirationDate", None),
            "ShouldDisplayExpirationDate": response["ShouldDisplayExpirationDate"],
            "Edition": getattr(response, "Edition", None),
        }

    def get_server_license_data_extended(self) -> dict:
        response = self.suds_client.execute(
            "GetServerLicenseDataExtended", sessionID="0"
        )
        supported_languages = response.SupportedLanguages
        return {
            "ExpirationDate": response["ExpirationDate"],
            "ExpirationDateIso": getattr(response, "ExpirationDateIso", None),
            "MaxConcurrentScans": response["MaxConcurrentScans"],
            "MaxLOC": response["MaxLOC"],
            "HID": response["HID"],
            "SupportedLanguages": (
                [
                    {"isSupported": item["isSupported"], "language": item["language"]}
                    for item in supported_languages["SupportedLanguage"]
                ]
                if supported_languages
                else None
            ),
            "MaxUsers": response["MaxUsers"],
            "CurrentUsers": response["CurrentUsers"],
            "MaxAuditUsers": response["MaxAuditUsers"],
            "CurrentAuditUsers": response["CurrentAuditUsers"],
            "IsOsaEnabled": response["IsOsaEnabled"],
            "OsaExpirationDate": response["OsaExpirationDate"],
            "Edition": response["Edition"],
            "ProjectsAllowed": response["ProjectsAllowed"],
            "CurrentProjectsCount": response["CurrentProjectsCount"],
        }

    def get_custom_fields(self) -> dict:
        response = self.suds_client.execute("GetCustomFields", sessionID="0")
        fields_array = getattr(response, "fieldsArray", None)
        items = (
            getattr(fields_array, "CxWSCustomField", [])
            if fields_array
            else []
        )
        return {
            "IsSuccesfull": response["IsSuccesfull"],
            "ErrorMessage": getattr(response, "ErrorMessage", None),
            "fieldsArray": [
                {
                    "Id": item.Id,
                    "Name": item.Name,
                    "IsMandatory": item.IsMandatory,
                }
                for item in (items if isinstance(items, list) else [items])
            ],
        }

    def get_custom_field_values(self, project_id: int, scan_id: int) -> dict:
        response = self.suds_client.execute(
            "GetCustomFieldValues",
            sessionID="0",
            projectID=project_id,
            scanID=scan_id,
        )
        return {
            "IsSuccesfull": response["IsSuccesfull"],
            "ErrorMessage": getattr(response, "ErrorMessage", None),
            "customFieldValues": getattr(response, "customFieldValues", None),
        }

    def get_result_paths_for_query(
        self, scan_id: int, query_id: int
    ) -> dict:
        response = self.suds_client.execute(
            "GetResultPathsForQuery",
            sessionId="0",
            scanId=scan_id,
            queryId=query_id,
        )
        paths = getattr(response, "Paths", None)
        items = getattr(paths, "CxWSResultPath", []) if paths else []
        return {
            "IsSuccesfull": response["IsSuccesfull"],
            "ErrorMessage": getattr(response, "ErrorMessage", None),
            "Paths": [
                {
                    "PathId": item.PathId,
                    "SimilarityId": item.SimilarityId,
                    "Nodes": getattr(item, "Nodes", None),
                }
                for item in (items if isinstance(items, list) else [items])
            ],
        }

    def get_results_for_query(
        self, scan_id: int, query_id: int
    ) -> dict:
        response = self.suds_client.execute(
            "GetResultsForQuery",
            sessionID="0",
            scanId=scan_id,
            queryId=query_id,
        )
        results = getattr(response, "Results", None)
        items = (
            getattr(results, "CxWSSingleResultData", [])
            if results
            else []
        )
        return {
            "IsSuccesfull": response["IsSuccesfull"],
            "ErrorMessage": getattr(response, "ErrorMessage", None),
            "Results": [
                {
                    "QueryId": item.QueryId,
                    "PathId": item.PathId,
                    "SourceFolder": item.SourceFolder,
                    "SourceFile": item.SourceFile,
                    "SourceLine": item.SourceLine,
                    "SourceObject": item.SourceObject,
                    "DestFolder": item.DestFolder,
                    "DestFile": item.DestFile,
                    "DestLine": item.DestLine,
                    "NumberOfNodes": item.NumberOfNodes,
                    "DestObject": item.DestObject,
                    "Comment": item.Comment,
                    "State": item.State,
                    "Severity": item.Severity,
                    "AssignedUser": item.AssignedUser,
                    "ConfidenceLevel": item.ConfidenceLevel,
                    "ResultStatus": item.ResultStatus,
                    "IssueTicketID": item.IssueTicketID,
                    "QueryVersionCode": item.QueryVersionCode,
                }
                for item in (items if isinstance(items, list) else [items])
            ],
        }

    def get_queries_for_scan(self, scan_id: int) -> dict:
        response = self.suds_client.execute(
            "GetQueriesForScan", sessionID="0", scanId=scan_id
        )
        query_groups = getattr(response, "QueryGroups", None)
        groups = (
            getattr(query_groups, "CxWSQueryGroup", [])
            if query_groups
            else []
        )
        return {
            "IsSuccesfull": response["IsSuccesfull"],
            "ErrorMessage": getattr(response, "ErrorMessage", None),
            "QueryGroups": [
                {
                    "Name": qg.Name,
                    "Language": qg.Language,
                    "LanguageName": qg.LanguageName,
                    "Queries": [
                        {
                            "QueryId": q.QueryId,
                            "Name": q.Name,
                            "Severity": q.Severity,
                        }
                        for q in (getattr(qg.Queries, "CxWSQuery", []) or [])
                    ],
                }
                for qg in (groups if isinstance(groups, list) else [groups])
            ],
        }

    def get_scan_properties(self, scan_id: int) -> dict:
        response = self.suds_client.execute(
            "GetScanProperties", sessionID="0", ScanID=scan_id
        )
        return {
            "IsSuccesfull": response["IsSuccesfull"],
            "ErrorMessage": getattr(response, "ErrorMessage", None),
            "ScanProperties": getattr(response, "ScanProperties", None),
        }

    def get_status_of_single_scan(self, scan_id: int) -> dict:
        response = self.suds_client.execute(
            "GetStatusOfSingleScan", sessionID="0", runId=str(scan_id)
        )
        return {
            "IsSuccesfull": response["IsSuccesfull"],
            "ErrorMessage": getattr(response, "ErrorMessage", None),
            "ScanStatus": getattr(response, "ScanStatus", None),
        }

    def get_scans_statuses(self) -> dict:
        response = self.suds_client.execute(
            "GetScansStatuses",
            sessionID="0",
        )
        statuses = getattr(response, "ScansStatusesList", None)
        items = (
            getattr(statuses, "ScanStatus", [])
            if statuses
            else []
        )
        return {
            "IsSuccesfull": response["IsSuccesfull"],
            "ErrorMessage": getattr(response, "ErrorMessage", None),
            "ScansStatusesList": [
                {
                    "ScanID": item.ScanID,
                    "Status": getattr(item, "Status", None),
                    "TotalPercent": item.TotalPercent,
                    "StagePercent": item.StagePercent,
                    "Stage": getattr(item, "Stage", None),
                }
                for item in (items if isinstance(items, list) else [items])
            ],
        }

    def get_scan_logs(self, scan_id: int) -> dict:
        response = self.suds_client.execute(
            "GetScanLogs", sessionID="0", scanId=scan_id
        )
        return {
            "IsSuccesfull": response["IsSuccesfull"],
            "ErrorMessage": getattr(response, "ErrorMessage", None),
            "ScanLogs": getattr(response, "ScanLogs", None),
        }

    def update_result_state(
        self,
        scan_id: int,
        path_id: int,
        project_id: int,
        remarks: str = "",
        result_label_type: str = "Remark",
        data: str = "",
    ) -> dict:
        response = self.suds_client.execute(
            "UpdateResultState",
            sessionID="0",
            scanId=scan_id,
            PathId=path_id,
            projectId=project_id,
            Remarks=remarks,
            ResultLabelType=result_label_type,
            data=data,
        )
        return {
            "IsSuccesfull": response["IsSuccesfull"],
            "ErrorMessage": getattr(response, "ErrorMessage", None),
        }

    def update_result_comment(
        self, result_id: int, path_id: int, project_id: int, comment: str
    ) -> dict:
        response = self.suds_client.execute(
            "UpdateResultComment",
            sessionID="0",
            ResultId=result_id,
            PathId=path_id,
            projectId=project_id,
            comment=comment,
        )
        return {
            "IsSuccesfull": response["IsSuccesfull"],
            "ErrorMessage": getattr(response, "ErrorMessage", None),
        }

    def update_scan_comment(self, scan_id: int, comment: str) -> dict:
        response = self.suds_client.execute(
            "UpdateScanComment",
            sessionID="0",
            ScanID=scan_id,
            Comment=comment,
        )
        return {
            "IsSuccesfull": response["IsSuccesfull"],
            "ErrorMessage": getattr(response, "ErrorMessage", None),
        }

    def is_valid_preset_name(self, name: str) -> dict:
        response = self.suds_client.execute(
            "IsValidPresetName", sessionID="0", presetName=name
        )
        return {
            "IsSuccesfull": response["IsSuccesfull"],
            "ErrorMessage": getattr(response, "ErrorMessage", None),
        }

    def get_server_language_list(self) -> dict:
        response = self.suds_client.execute(
            "GetServerLanguageList", sessionID="0"
        )
        lang_list = getattr(response, "LanguageList", None)
        items = (
            getattr(lang_list, "CxWSProjectLanguage", [])
            if lang_list
            else []
        )
        return {
            "IsSuccesfull": response["IsSuccesfull"],
            "ErrorMessage": getattr(response, "ErrorMessage", None),
            "LanguageList": [
                {
                    "LanguageName": item.LanguageName,
                    "LanguageOrder": getattr(item, "LanguageOrder", None),
                }
                for item in (items if isinstance(items, list) else [items])
            ],
        }

    def get_executable_list(self) -> dict:
        response = self.suds_client.execute(
            "GetExecutableList", sessionId="0"
        )
        exec_list = getattr(response, "ExecutableList", None)
        items = (
            getattr(exec_list, "CxWSExecutable", [])
            if exec_list
            else []
        )
        return {
            "IsSuccesfull": response["IsSuccesfull"],
            "ErrorMessage": getattr(response, "ErrorMessage", None),
            "ExecutableList": [
                {
                    "ExecutableName": item.ExecutableName,
                    "ExeSettings": getattr(item, "ExeSettings", None),
                }
                for item in (items if isinstance(items, list) else [items])
            ],
        }

    def count_lines(self, source_code: str, language_name: str) -> dict:
        response = self.suds_client.execute(
            "CountLines",
            sessionID="0",
            sourceCode=source_code,
            languageName=language_name,
        )
        return {
            "IsSuccesfull": response["IsSuccesfull"],
            "ErrorMessage": getattr(response, "ErrorMessage", None),
            "LineCount": getattr(response, "LineCount", None),
        }

    def is_alive(self) -> dict:
        response = self.suds_client._client.service.IsAlive()
        return {
            "IsSuccesfull": bool(response),
            "ErrorMessage": None,
        }

    def is_smtp_host_configured(self) -> dict:
        response = self.suds_client.execute("IsSMTPHostConfigured")
        return {
            "IsSuccesfull": response["IsSuccesfull"],
            "ErrorMessage": getattr(response, "ErrorMessage", None),
        }

    def is_private_cloud(self) -> dict:
        response = self.suds_client.execute("IsPrivateCloud")
        return {
            "IsSuccesfull": response["IsSuccesfull"],
            "ErrorMessage": getattr(response, "ErrorMessage", None),
        }

    def get_cwe_description(self, cwe_id: int) -> dict:
        response = self.suds_client.execute(
            "GetCWEDescription", sessionId="0", cweID=cwe_id
        )
        return {
            "IsSuccesfull": response["IsSuccesfull"],
            "ErrorMessage": getattr(response, "ErrorMessage", None),
            "CWEDescription": getattr(response, "CWEDescription", None),
        }

    def get_result_state_flags(self) -> dict:
        response = self.suds_client.execute(
            "GetResultStateFlags", sessionID="0"
        )
        return {
            "IsSuccesfull": response["IsSuccesfull"],
            "ErrorMessage": getattr(response, "ErrorMessage", None),
        }

    def cancel_scan(self, scan_id: int) -> dict:
        response = self.suds_client.execute(
            "CancelScan", SessionID="0", scanID=scan_id
        )
        return {
            "IsSuccesfull": response["IsSuccesfull"],
            "ErrorMessage": getattr(response, "ErrorMessage", None),
        }

    def delete_scan(self, scan_id: int) -> dict:
        response = self.suds_client.execute(
            "DeleteScan", sessionID="0", scanID=scan_id
        )
        return {
            "IsSuccesfull": response["IsSuccesfull"],
            "ErrorMessage": getattr(response, "ErrorMessage", None),
        }

    def delete_scans(self, scan_ids: list) -> dict:
        factory = self.suds_client.factory
        scan_id_list = factory.ArrayOfLong(scan_ids)
        response = self.suds_client.execute(
            "DeleteScans", sessionID="0", scanIDs=scan_id_list
        )
        return {
            "IsSuccesfull": response["IsSuccesfull"],
            "ErrorMessage": getattr(response, "ErrorMessage", None),
        }

    def get_child_nodes(
        self, team_id: str = "", level: int = 0, team_path: str = ""
    ) -> dict:
        response = self.suds_client.execute(
            "GetChildNodes",
            sessionID="0",
            pTeamId=team_id,
            pLevel=level,
            pTeamPath=team_path,
        )
        return {
            "IsSuccesfull": response["IsSuccesfull"],
            "ErrorMessage": getattr(response, "ErrorMessage", None),
            "ChildNodes": getattr(response, "ChildNodes", None),
        }

    def get_projects_with_scans(self) -> dict:
        response = self.suds_client.execute(
            "GetProjectsWithScans", sessionId="0"
        )
        project_list = getattr(response, "projectList", None)
        items = (
            getattr(project_list, "ProjectDisplayData", [])
            if project_list
            else []
        )
        return {
            "IsSuccesfull": response["IsSuccesfull"],
            "ErrorMessage": getattr(response, "ErrorMessage", None),
            "projectList": [
                {
                    "ProjectName": item.ProjectName,
                    "projectID": item.projectID,
                    "Group": item.Group,
                    "TotalScans": item.TotalScans,
                    "LastScanDate": getattr(item, "LastScanDate", None),
                    "Owner": item.Owner,
                }
                for item in (items if isinstance(items, list) else [items])
            ],
        }

    def get_configuration_set_list(self) -> dict:
        response = self.suds_client.execute(
            "GetConfigurationSetList", SessionID="0"
        )
        config_list = getattr(response, "ConfigSetList", None)
        items = (
            getattr(config_list, "ConfigurationSet", [])
            if config_list
            else []
        )
        return {
            "IsSuccesfull": response["IsSuccesfull"],
            "ErrorMessage": getattr(response, "ErrorMessage", None),
            "ConfigSetList": [
                {
                    "ID": item.ID,
                    "ConfigSetName": item.ConfigSetName,
                }
                for item in (items if isinstance(items, list) else [items])
            ],
        }


def add_license_expiration_notification() -> dict:
    return CxPortalWebService().add_license_expiration_notification()


def create_new_preset(query_ids: List[str], name: str) -> dict:
    return CxPortalWebService().create_new_preset(query_ids=query_ids, name=name)


def create_scan_report(
    scan_id,
    report_type,
    queries_all=True,
    queries_ids=None,
    results_severity_all=True,
    results_severity_criticl=True,
    results_severity_high=True,
    results_severity_medium=True,
    results_severity_low=True,
    results_severity_info=False,
    results_state_all=True,
    results_state_ids=None,
    display_categories_all=True,
    display_categories_ids=None,
    results_assigned_to_all=True,
    results_assigned_to_ids=None,
    results_assigned_to_usernames=None,
    results_per_vulnerability_all=True,
    results_per_vulnerability_maximum=50,
    header_options_link_to_online_results=True,
    header_options_team=True,
    header_options_checkmarx_version=True,
    header_options_comments=False,
    header_options_scan_custom_fields=True,
    header_options_scan_type=True,
    header_options_source_origin=True,
    header_options_density=True,
    general_options_only_executive_summary=False,
    general_options_table_of_contents=True,
    general_options_executive_summary=True,
    general_options_display_categories=True,
    general_options_display_language_hash_number=True,
    general_options_scanned_queries=False,
    general_options_scanned_files=False,
    general_options_vulnerabilities_description="Attached2Appendix",
    results_display_option_assigned_to=False,
    results_display_option_comments=False,
    results_display_option_link_to_online=True,
    results_display_option_result_description=True,
    results_display_option_snippets_mode="SourceAndDestination",
) -> dict:
    return CxPortalWebService().create_scan_report(
        scan_id=scan_id,
        report_type=report_type,
        queries_all=queries_all,
        queries_ids=queries_ids,
        results_severity_all=results_severity_all,
        results_severity_criticl=results_severity_criticl,
        results_severity_high=results_severity_high,
        results_severity_medium=results_severity_medium,
        results_severity_low=results_severity_low,
        results_severity_info=results_severity_info,
        results_state_all=results_state_all,
        results_state_ids=results_state_ids,
        display_categories_all=display_categories_all,
        display_categories_ids=display_categories_ids,
        results_assigned_to_all=results_assigned_to_all,
        results_assigned_to_ids=results_assigned_to_ids,
        results_assigned_to_usernames=results_assigned_to_usernames,
        results_per_vulnerability_all=results_per_vulnerability_all,
        results_per_vulnerability_maximum=results_per_vulnerability_maximum,
        header_options_link_to_online_results=header_options_link_to_online_results,
        header_options_team=header_options_team,
        header_options_checkmarx_version=header_options_checkmarx_version,
        header_options_comments=header_options_comments,
        header_options_scan_custom_fields=header_options_scan_custom_fields,
        header_options_scan_type=header_options_scan_type,
        header_options_source_origin=header_options_source_origin,
        header_options_density=header_options_density,
        general_options_only_executive_summary=general_options_only_executive_summary,
        general_options_table_of_contents=general_options_table_of_contents,
        general_options_executive_summary=general_options_executive_summary,
        general_options_display_categories=general_options_display_categories,
        general_options_display_language_hash_number=general_options_display_language_hash_number,
        general_options_scanned_queries=general_options_scanned_queries,
        general_options_scanned_files=general_options_scanned_files,
        general_options_vulnerabilities_description=general_options_vulnerabilities_description,
        results_display_option_assigned_to=results_display_option_assigned_to,
        results_display_option_comments=results_display_option_comments,
        results_display_option_link_to_online=results_display_option_link_to_online,
        results_display_option_result_description=results_display_option_result_description,
        results_display_option_snippets_mode=results_display_option_snippets_mode,
    )


def delete_preset(preset_id: int) -> dict:
    return CxPortalWebService().delete_preset(preset_id=preset_id)


def delete_project(project_id: int) -> dict:
    return CxPortalWebService().delete_project(project_id=project_id)


def delete_projects(project_ids: List[int], flag: str = "None") -> dict:
    return CxPortalWebService().delete_projects(project_ids=project_ids, flag=flag)


def export_preset(preset_id: int) -> dict:
    return CxPortalWebService().export_preset(preset_id=preset_id)


def export_queries(queries_ids: List[int]) -> dict:
    return CxPortalWebService().export_queries(queries_ids=queries_ids)


def get_associated_group_list() -> dict:
    return CxPortalWebService().get_associated_group_list()


def get_compare_scan_results(old_scan_id: int, new_scan_id: int) -> dict:
    return CxPortalWebService().get_compare_scan_results(
        old_scan_id=old_scan_id, new_scan_id=new_scan_id
    )


def get_import_queries_status(request_id: int) -> dict:
    return CxPortalWebService().get_import_queries_status(request_id=request_id)


def get_path_comments_history(scan_id: int, path_id: int, label_type: str) -> dict:
    return CxPortalWebService().get_path_comments_history(
        scan_id=scan_id, path_id=path_id, label_type=label_type
    )


def get_pivot_data(
    pivot_view_client_type: str,
    include_not_exploitable: bool = False,
    range_type: str = "PAST_MONTH",
    date_from: str = None,
    date_to: str = None,
) -> dict:
    return CxPortalWebService().get_pivot_data(
        pivot_view_client_type=pivot_view_client_type,
        include_not_exploitable=include_not_exploitable,
        range_type=range_type,
        date_from=date_from,
        date_to=date_to,
    )


def get_queries_categories() -> dict:
    return CxPortalWebService().get_queries_categories()


def get_query_collection() -> dict:
    return CxPortalWebService().get_query_collection()


def get_query_id_by_language_group_and_query_name(
    query_collections: List[dict],
    language: str,
    package_type_name: str,
    package_name: str,
    query_name: str,
) -> Union[int, None]:
    return CxPortalWebService().get_query_id_by_language_group_and_query_name(
        query_collections=query_collections,
        language=language,
        package_type_name=package_type_name,
        package_name=package_name,
        query_name=query_name,
    )


def get_query_description_by_query_id(query_id: int) -> dict:
    return CxPortalWebService().get_query_description_by_query_id(query_id=query_id)


def get_cx_description_by_query_id():
    return CxPortalWebService().get_cx_description_by_query_id()


def get_name_of_user_who_marked_false_positive_from_comments_history(
    scan_id: int, path_id: int
) -> Union[str, None]:
    return CxPortalWebService().get_name_of_user_who_marked_false_positive_from_comments_history(
        scan_id=scan_id, path_id=path_id
    )


def get_preset_list() -> dict:
    return CxPortalWebService().get_preset_list()


def get_projects_display_data() -> dict:
    return CxPortalWebService().get_projects_display_data()


def get_result_path(scan_id: int, path_id: int) -> dict:
    return CxPortalWebService().get_result_path(scan_id=scan_id, path_id=path_id)


def get_results_for_scan(scan_id: int) -> dict:
    return CxPortalWebService().get_results_for_scan(scan_id=scan_id)


def get_server_license_data() -> dict:
    return CxPortalWebService().get_server_license_data()


def get_server_license_summary() -> dict:
    return CxPortalWebService().get_server_license_summary()


def get_user_profile_data() -> dict:
    return CxPortalWebService().get_user_profile_data()


def get_version_number() -> dict:
    return CxPortalWebService().get_version_number()


def get_version_number_as_int() -> int:
    return CxPortalWebService().get_version_number_as_int()


def import_preset(imported_file_path: str) -> Union[dict, None]:
    return CxPortalWebService().import_preset(imported_file_path=imported_file_path)


def import_queries(imported_file_path: str) -> Union[dict, None]:
    return CxPortalWebService().import_queries(imported_file_path=imported_file_path)


def lock_scan(scan_id: int) -> dict:
    return CxPortalWebService().lock_scan(scan_id=scan_id)


def postpone_scan(scan_id: int) -> dict:
    return CxPortalWebService().postpone_scan(scan_id=scan_id)


def get_source_by_scan_id(scan_id: int, file_name: str) -> dict:
    return CxPortalWebService().get_source_by_scan_id(
        scan_id=scan_id, file_name=file_name
    )


def get_sources_by_scan_id(scan_id: int, file_names: list) -> dict:
    return CxPortalWebService().get_sources_by_scan_id(
        scan_id=scan_id, file_names=file_names
    )


def get_file_names_for_path(scan_id: int, path_id: int) -> dict:
    return CxPortalWebService().get_file_names_for_path(
        scan_id=scan_id, path_id=path_id
    )


def unlock_scan(scan_id: int) -> dict:
    return CxPortalWebService().unlock_scan(scan_id=scan_id)


def get_preset_details(preset_id: int) -> dict:
    return CxPortalWebService().get_preset_details(preset_id=preset_id)


def update_preset(preset_id: int, query_ids: list, name: str) -> dict:
    return CxPortalWebService().update_preset(
        preset_id=preset_id, query_ids=query_ids, name=name
    )


def get_result_state_list() -> dict:
    return CxPortalWebService().get_result_state_list()


def get_scan_report(report_id: int) -> dict:
    return CxPortalWebService().get_scan_report(report_id=report_id)


def get_scan_report_status(report_id: int) -> dict:
    return CxPortalWebService().get_scan_report_status(report_id=report_id)


def cancel_scan_report(report_id: int) -> dict:
    return CxPortalWebService().cancel_scan_report(report_id=report_id)


def get_results(scan_id: int) -> dict:
    return CxPortalWebService().get_results(scan_id=scan_id)


def get_result_summary(scan_id: int) -> dict:
    return CxPortalWebService().get_result_summary(scan_id=scan_id)


def get_query_collection_for_language(
    project_type: str = "Regular", project_id: int = 0
) -> dict:
    return CxPortalWebService().get_query_collection_for_language(
        project_type=project_type, project_id=project_id
    )


def get_query_description(cwe_id: int) -> dict:
    return CxPortalWebService().get_query_description(cwe_id=cwe_id)


def get_query_short_description(query_id: int) -> dict:
    return CxPortalWebService().get_query_short_description(query_id=query_id)


def get_scans_display_data_for_all_projects() -> dict:
    return CxPortalWebService().get_scans_display_data_for_all_projects()


def get_scan_summary(scan_id: int) -> dict:
    return CxPortalWebService().get_scan_summary(scan_id=scan_id)


def get_server_license_basic() -> dict:
    return CxPortalWebService().get_server_license_basic()


def get_server_license_data_extended() -> dict:
    return CxPortalWebService().get_server_license_data_extended()


def get_custom_fields() -> dict:
    return CxPortalWebService().get_custom_fields()


def get_custom_field_values(project_id: int, scan_id: int) -> dict:
    return CxPortalWebService().get_custom_field_values(
        project_id=project_id, scan_id=scan_id
    )


def get_result_paths_for_query(scan_id: int, query_id: int) -> dict:
    return CxPortalWebService().get_result_paths_for_query(
        scan_id=scan_id, query_id=query_id
    )


def get_results_for_query(scan_id: int, query_id: int) -> dict:
    return CxPortalWebService().get_results_for_query(
        scan_id=scan_id, query_id=query_id
    )


def get_queries_for_scan(scan_id: int) -> dict:
    return CxPortalWebService().get_queries_for_scan(scan_id=scan_id)


def get_scan_properties(scan_id: int) -> dict:
    return CxPortalWebService().get_scan_properties(scan_id=scan_id)


def get_status_of_single_scan(scan_id: int) -> dict:
    return CxPortalWebService().get_status_of_single_scan(scan_id=scan_id)


def get_scans_statuses() -> dict:
    return CxPortalWebService().get_scans_statuses()


def get_scan_logs(scan_id: int) -> dict:
    return CxPortalWebService().get_scan_logs(scan_id=scan_id)


def update_result_state(
    scan_id: int,
    path_id: int,
    project_id: int,
    remarks: str = "",
    result_label_type: str = "Remark",
    data: str = "",
) -> dict:
    return CxPortalWebService().update_result_state(
        scan_id=scan_id,
        path_id=path_id,
        project_id=project_id,
        remarks=remarks,
        result_label_type=result_label_type,
        data=data,
    )


def update_result_comment(
    result_id: int, path_id: int, project_id: int, comment: str
) -> dict:
    return CxPortalWebService().update_result_comment(
        result_id=result_id, path_id=path_id, project_id=project_id, comment=comment
    )


def update_scan_comment(scan_id: int, comment: str) -> dict:
    return CxPortalWebService().update_scan_comment(scan_id=scan_id, comment=comment)


def is_valid_preset_name(name: str) -> dict:
    return CxPortalWebService().is_valid_preset_name(name=name)


def get_server_language_list() -> dict:
    return CxPortalWebService().get_server_language_list()


def get_executable_list() -> dict:
    return CxPortalWebService().get_executable_list()


def count_lines(source_code: str, language_name: str) -> dict:
    return CxPortalWebService().count_lines(
        source_code=source_code, language_name=language_name
    )


def is_alive() -> dict:
    return CxPortalWebService().is_alive()


def is_smtp_host_configured() -> dict:
    return CxPortalWebService().is_smtp_host_configured()


def is_private_cloud() -> dict:
    return CxPortalWebService().is_private_cloud()


def get_cwe_description(cwe_id: int) -> dict:
    return CxPortalWebService().get_cwe_description(cwe_id=cwe_id)


def get_result_state_flags() -> dict:
    return CxPortalWebService().get_result_state_flags()


def cancel_scan(scan_id: int) -> dict:
    return CxPortalWebService().cancel_scan(scan_id=scan_id)


def delete_scan(scan_id: int) -> dict:
    return CxPortalWebService().delete_scan(scan_id=scan_id)


def delete_scans(scan_ids: list) -> dict:
    return CxPortalWebService().delete_scans(scan_ids=scan_ids)


def get_child_nodes(
    team_id: str = "", level: int = 0, team_path: str = ""
) -> dict:
    return CxPortalWebService().get_child_nodes(
        team_id=team_id, level=level, team_path=team_path
    )


def get_projects_with_scans() -> dict:
    return CxPortalWebService().get_projects_with_scans()


def get_configuration_set_list() -> dict:
    return CxPortalWebService().get_configuration_set_list()
