# encoding: utf-8
"""
    Portal SOAP API
    Only support 9.x version.
    Start from 9.0, Portal SOAP API needs Bear Token for authentication
"""
from os.path import exists

from .zeepClient import get_client_and_factory, retry_when_unauthorized

relative_web_interface_url = "/CxWebInterface/Portal/CxWebService.asmx?wsdl"


def add_license_expiration_notification():
    """

    Returns:

    """

    @retry_when_unauthorized
    def execute():
        client, factory = get_client_and_factory(relative_web_interface_url=relative_web_interface_url)
        return client.service.AddLicenseExpirationNotification(sessionID="0")

    response = execute()

    return {
        "IsSuccesfull": response["IsSuccesfull"],
        "ErrorMessage": response["ErrorMessage"]
    }


def create_new_preset(query_ids, name):
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

    @retry_when_unauthorized
    def execute():
        client, factory = get_client_and_factory(relative_web_interface_url=relative_web_interface_url)
        query_id_list = factory.ArrayOfLong(query_ids)

        cx_preset_detail = factory.CxPresetDetails(
            queryIds=query_id_list, id=0, name=name, owningteam=1, isPublic=True,
            isUserAllowToUpdate=True, isUserAllowToDelete=True, IsDuplicate=False
        )

        return client.service.CreateNewPreset(sessionId="0", presrt=cx_preset_detail)

    response = execute()
    preset = response.preset
    return {
        "IsSuccesfull": response["IsSuccesfull"],
        "ErrorMessage": response["ErrorMessage"],
        "preset": {
            'queryIds': preset["queryIds"]["long"],
            'id': preset["id"],
            'name': preset["name"],
            'owningteam': preset["owningteam"],
            'isPublic': preset["isPublic"],
            'owner': preset["owner"],
            'isUserAllowToUpdate': preset["isUserAllowToUpdate"],
            'isUserAllowToDelete': preset["isUserAllowToDelete"],
            'IsDuplicate': preset["IsDuplicate"]
        } if preset else None
    }


def create_scan_report(scan_id, report_type, queries_all=True, queries_ids=None, results_severity_all=True,
                       results_severity_high=True, results_severity_medium=True, results_severity_low=True,
                       results_severity_info=False, results_state_all=True, results_state_ids=None,
                       display_categories_all=True, display_categories_ids=None, results_assigned_to_all=True,
                       results_assigned_to_ids=None, results_assigned_to_usernames=None,
                       results_per_vulnerability_all=True, results_per_vulnerability_maximum=50,
                       header_options_link_to_online_results=True, header_options_team=True,
                       header_options_checkmarx_version=True, header_options_comments=False,
                       header_options_scan_custom_fields=True,
                       header_options_scan_type=True, header_options_source_origin=True, header_options_density=True,
                       general_options_only_executive_summary=False, general_options_table_of_contents=True,
                       general_options_executive_summary=True, general_options_display_categories=True,
                       general_options_display_language_hash_number=True, general_options_scanned_queries=False,
                       general_options_scanned_files=False,
                       general_options_vulnerabilities_description="Attached2Appendix",
                       results_display_option_assigned_to=False, results_display_option_comments=False,
                       results_display_option_link_to_online=True, results_display_option_result_description=True,
                       results_display_option_snippets_mode="SourceAndDestination"):
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

    @retry_when_unauthorized
    def execute():
        client, factory = get_client_and_factory(relative_web_interface_url=relative_web_interface_url)
        query_ids = queries_ids
        if queries_ids:
            query_ids = factory.ArrayOfLong(queries_ids)
        queries = factory.CxWSQueriesFilter(All=queries_all, IDs=query_ids)

        results_severity = factory.CxWSResultsSeverityFilter(
            All=results_severity_all, High=results_severity_high, Medium=results_severity_medium,
            Low=results_severity_low, Info=results_severity_info
        )

        results_state_id_list = results_state_ids
        if results_state_id_list:
            results_state_id_list = factory.ArrayOfLong(results_state_id_list)
        results_state = factory.CxWSResultsStateFilter(All=results_state_all, IDs=results_state_id_list)

        display_categories_id_list = display_categories_ids
        if display_categories_id_list:
            display_categories_id_list = factory.ArrayOfLong(display_categories_id_list)
        display_categories = factory.CxWSDisplayCategoriesFilter(
            All=display_categories_all, IDs=display_categories_id_list
        )

        results_assigned_to_id_list = results_assigned_to_ids
        if results_assigned_to_id_list:
            results_assigned_to_id_list = factory.ArrayOfLong(results_assigned_to_id_list)
        results_assigned_to_username_list = results_assigned_to_usernames
        if results_assigned_to_username_list:
            results_assigned_to_username_list = factory.ArrayOfString(results_assigned_to_username_list)

        results_assigned_to = factory.CxWSResultsAssignedToFilter(
            All=results_assigned_to_all, IDs=results_assigned_to_id_list, Usernames=results_assigned_to_username_list
        )

        results_per_vulnerability = factory.CxWSResultsPerVulnerabilityFilter(
            All=results_per_vulnerability_all, Maximimum=results_per_vulnerability_maximum
        )

        version = get_version_number_as_int()

        if version < 940:
            header_options = factory.CxWSHeaderDisplayOptions(
                Link2OnlineResults=header_options_link_to_online_results,
                Team=header_options_team,
                CheckmarxVersion=header_options_checkmarx_version,
                ScanComments=header_options_comments,
                ScanType=header_options_scan_type,
                SourceOrigin=header_options_source_origin,
                ScanDensity=header_options_density
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
                ScanDensity=header_options_density
            )

        general_option = factory.CxWSGeneralDisplayOptions(
            OnlyExecutiveSummary=general_options_only_executive_summary,
            TableOfContents=general_options_table_of_contents,
            ExecutiveSummary=general_options_executive_summary,
            DisplayCategories=general_options_display_categories,
            DisplayLanguageHashNumber=general_options_display_language_hash_number,
            ScannedQueries=general_options_scanned_queries,
            ScannedFiles=general_options_scanned_files,
            VulnerabilitiesDescription=general_options_vulnerabilities_description
        )

        results_display_option = factory.CxWSResultDisplayOptions(
            AssignedTo=results_display_option_assigned_to,
            Comments=results_display_option_comments,
            Link2Online=results_display_option_link_to_online,
            ResultDescription=results_display_option_result_description,
            SnippetsMode=results_display_option_snippets_mode
        )

        display_data = factory.CxWSReportDisplayData(
            Queries=queries, ResultsSeverity=results_severity, ResultsState=results_state,
            DisplayCategories=display_categories, ResultsAssigedTo=results_assigned_to,
            ResultsPerVulnerability=results_per_vulnerability, HeaderOptions=header_options,
            GeneralOption=general_option, ResultsDisplayOption=results_display_option
        )
        filtered_report_request = factory.CxWSFilteredReportRequest(Type=report_type, ScanID=scan_id,
                                                                    DisplayData=display_data)
        return client.service.CreateScanReport(SessionID="0", Report=filtered_report_request)

    response = execute()

    return {
        "IsSuccesfull": response["IsSuccesfull"],
        "ErrorMessage": response["ErrorMessage"],
        "ID": response["ID"]
    }


def delete_preset(preset_id):
    """

    Args:
        preset_id (int):

    Returns:

    """

    @retry_when_unauthorized
    def execute():
        client, factory = get_client_and_factory(relative_web_interface_url=relative_web_interface_url)
        return client.service.DeletePreset(sessionId="0", id=preset_id)

    response = execute()
    return {
        "IsSuccesfull": response["IsSuccesfull"],
        "ErrorMessage": response["ErrorMessage"]
    }


def delete_project(project_id):
    """

    Args:
        project_id (int):

    Returns:

    """

    @retry_when_unauthorized
    def execute():
        client, factory = get_client_and_factory(relative_web_interface_url=relative_web_interface_url)
        return client.service.DeleteProject(sessionID="0", projectID=project_id)

    response = execute()
    return {
        "IsSuccesfull": response["IsSuccesfull"],
        "ErrorMessage": response["ErrorMessage"]
    }


def delete_projects(project_ids, flag="None"):
    """

    Args:
        project_ids (list of int):
        flag (str): "None", "RunningScans", "OnlyAllowedProjects"

    Returns:
        bool
    """

    @retry_when_unauthorized
    def execute():
        client, factory = get_client_and_factory(relative_web_interface_url=relative_web_interface_url)
        cx_ws_request_delete_projects = factory.CxWSRequestDeleteProjects(
            SessionID="0",
            ProjectIDs=factory.ArrayOfLong(project_ids),
            Flags=factory.DeleteFlags([flag])
        )
        return client.service.DeleteProjects(request=cx_ws_request_delete_projects)

    response = execute()
    return {
        "IsSuccesfull": response["IsSuccesfull"],
        "ErrorMessage": response["ErrorMessage"],
        "Flags": response["Flags"],
        "IsConfirmation": response["IsConfirmation"],
        "NumOfDeletedProjects": response["NumOfDeletedProjects"],
        "UndeletedProjects": response["UndeletedProjects"]
    }


def export_preset(preset_id):
    """

    Args:
        preset_id (int):

    Returns:

    """

    @retry_when_unauthorized
    def execute():
        client, factory = get_client_and_factory(relative_web_interface_url=relative_web_interface_url)
        return client.service.ExportPreset(sessionId="0", presetId=preset_id)

    response = execute()

    return {
        "IsSuccesfull": response["IsSuccesfull"],
        "ErrorMessage": response["ErrorMessage"],
        "OverridenCorpQueryNames": response["OverridenCorpQueryNames"]["string"],
        "Preset": response["Preset"]
    }


def export_queries(queries_ids):
    """

    Args:
        queries_ids:

    Returns:

    """

    @retry_when_unauthorized
    def execute():
        client, factory = get_client_and_factory(relative_web_interface_url=relative_web_interface_url)
        query_ids = queries_ids
        if queries_ids:
            query_ids = factory.ArrayOfLong(queries_ids)
        return client.service.ExportQueries(sessionId="0", queryIds=query_ids)

    response = execute()

    return {
        "IsSuccesfull": response["IsSuccesfull"],
        "ErrorMessage": response["ErrorMessage"],
        "Queries": response["Queries"]
    }


def get_associated_group_list():
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
    @retry_when_unauthorized
    def execute():
        client, factory = get_client_and_factory(relative_web_interface_url=relative_web_interface_url)
        return client.service.GetAssociatedGroupsList(SessionID="0")

    response = execute()
    group_list = response.GroupList
    return {
        "IsSuccesfull": response["IsSuccesfull"],
        "ErrorMessage": response["ErrorMessage"],
        "GroupList": [
            {
                "FullPath": item["FullPath"],
                "GroupName": item["GroupName"],
                "Guid": item["Guid"],
                "ID": item["ID"],
                "Path": item["Path"],
                "Type": item["Type"],
            } for item in group_list.Group
        ] if group_list else None
    }


def get_compare_scan_results(old_scan_id, new_scan_id):
    """

    Args:
        old_scan_id (int):
        new_scan_id (int):

    Returns:

    """

    @retry_when_unauthorized
    def execute():
        client, _ = get_client_and_factory(relative_web_interface_url=relative_web_interface_url)
        return client.service.GetCompareScanResults(sessionId="0", oldScanId=old_scan_id, newScanId=new_scan_id)

    response = execute()
    return {
        "IsSuccesfull": response["IsSuccesfull"],
        "ErrorMessage": response["ErrorMessage"],
        "Results": [
            {
                'QueryId': item.QueryId,
                'PathId': item.PathId,
                'SourceFolder': item.SourceFolder,
                'SourceFile': item.SourceFile,
                'SourceLine': item.SourceLine,
                'SourceObject': item.SourceObject,
                'DestFolder': item.DestFolder,
                'DestFile': item.DestFile,
                'DestLine': item.DestLine,
                'NumberOfNodes': item.NumberOfNodes,
                'DestObject': item.DestObject,
                'Comment': item.Comment,
                'State': item.State,
                'Severity': item.Severity,
                'AssignedUser': item.AssignedUser,
                'ConfidenceLevel': item.ConfidenceLevel,
                'ResultStatus': item.ResultStatus,
                'IssueTicketID': item.IssueTicketID,
                'QueryVersionCode': item.QueryVersionCode,
                'ScanId': item.ScanId,
                'ComparedToScanId': item.ComparedToScanId,
                'ComparedToScanPathId': item.ComparedToScanPathId,
                'QueryName': item.QueryName,
            } for item in response["Results"]["CxWSSingleResultCompareData"]
        ]
    }


def get_import_queries_status(request_id):
    """

    Args:
        request_id (int):

    Returns:

    """
    @retry_when_unauthorized
    def execute():
        client, factory = get_client_and_factory(relative_web_interface_url=relative_web_interface_url)
        return client.service.GetImportQueriesStatus(sessionId="0", requestId=request_id)

    response = execute()
    return {
        "IsSuccesfull": response["IsSuccesfull"],
        "ErrorMessage": response["ErrorMessage"],
        "requestId": response["requestId"],
        "importQueryStatus": response["importQueryStatus"]
    }


def get_path_comments_history(scan_id, path_id, label_type):
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

    @retry_when_unauthorized
    def execute():
        client, factory = get_client_and_factory(relative_web_interface_url=relative_web_interface_url)
        return client.service.GetPathCommentsHistory(sessionId="0", scanId=scan_id, pathId=path_id,
                                                     labelType=label_type)

    response = execute()
    path = response.Path
    return {
        "IsSuccesfull": response["IsSuccesfull"],
        "ErrorMessage": response["ErrorMessage"],
        "Path": {
            "AssignedUser": path["AssignedUser"],
            "Comment": path["Comment"],
            "Nodes": path["Nodes"],
            "PathId": path["PathId"],
            "Severity": path["Severity"],
            "SimilarityId": path["SimilarityId"],
            "State": path["State"]
        } if path else None
    }


def get_queries_categories():
    """

    Returns:

    """

    @retry_when_unauthorized
    def execute():
        client, factory = get_client_and_factory(relative_web_interface_url=relative_web_interface_url)
        return client.service.GetQueriesCategories(sessionId="0")

    response = execute()
    categories = response.QueriesCategories.CxQueryCategory
    return {
        "IsSuccesfull": response["IsSuccesfull"],
        "ErrorMessage": response["ErrorMessage"],
        "QueriesCategories": [
            {
                "Id": category["Id"],
                "CategoryName": category["CategoryName"],
                "CategoryType": {
                    "Id": category["CategoryType"]["Id"],
                    "Name": category["CategoryType"]["Name"],
                    "Order": category["CategoryType"]["Order"]
                }
            } for category in categories
        ] if categories else None
    }


def get_query_collection():
    @retry_when_unauthorized
    def execute():
        client, factory = get_client_and_factory(relative_web_interface_url=relative_web_interface_url)
        return client.service.GetQueryCollection(sessionId="0")

    response = execute()
    return {
        "IsSuccesfull": response.IsSuccesfull,
        "ErrorMessage": response.ErrorMessage,
        "QueryGroups": [
            {
                "Description": query_group.Description,
                "Impacts": query_group.Impacts,
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
                "Queries": [
                    {
                        "Categories": [
                            {
                                "CategoryName": category.CategoryName,
                                "CategoryType": {
                                    "Id": category.CategoryType.Id,
                                    "Name": category.CategoryType.Name,
                                    "Order": category.CategoryType.Order,
                                },
                                "Id": category.Id
                            } for category in query.Categories.CxQueryCategory
                        ] if query.Categories else query.Categories,
                        "Cwe": query.Cwe,
                        "CxDescriptionID": query.CxDescriptionID,
                        "EngineMetadata": query.EngineMetadata,
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
                    } for query in query_group.Queries.CxWSQuery
                ],
                "Status": query_group.Status
            } for query_group in response.QueryGroups.CxWSQueryGroup
        ]
    }


def get_query_id_by_language_group_and_query_name(
        language=None, package_type_name=None, package_name=None, query_name=None
):
    """

    Args:
        language (str, list, tuple, None):
        package_type_name (str, list, tuple, None): ["Cx", "Corp"]
        package_name (str, list, tuple, None):
        query_name (str, list, tuple, None):

    Returns:
        int, list of int, None
    """
    query_id_list = []
    response = get_query_collection()
    if not response.get("IsSuccesfull"):
        return None

    query_collection = response.get("QueryGroups")

    if isinstance(language, str):
        query_collection = [item for item in query_collection if item.get("LanguageName") == language]
    elif isinstance(language, (list, tuple)):
        query_collection = [item for item in query_collection if item.get("LanguageName") in language]

    if isinstance(package_type_name, str):
        query_collection = [item for item in query_collection if item.get("PackageTypeName") == package_type_name]
    elif isinstance(package_type_name, (list, tuple)):
        query_collection = [item for item in query_collection if item.get("PackageTypeName") in package_type_name]

    if isinstance(package_name, str):
        query_collection = [item for item in query_collection if item.get("Name") == package_name]
    elif isinstance(package_name, (list, tuple)):
        query_collection = [item for item in query_collection if item.get("Name") in package_name]

    for item in query_collection:
        for query in item.get("Queries"):
            if isinstance(query_name, (str, list, tuple)) and query.get("Name") not in [query_name]:
                continue
            query_id = query.get("QueryId")
            query_id_list.append(query_id)

    if len(query_id_list) == 1:
        query_id_list = query_id_list[0]

    return query_id_list


def get_name_of_user_who_marked_false_positive_from_comments_history(scan_id, path_id):
    """

    Args:
        scan_id (int):
        path_id (int):

    Returns:
        first_and_last_name (str)
        example:
         "happy yang"
    """
    comments_history = get_path_comments_history(scan_id, path_id, label_type="Remark").get("Path").get("Comment")

    if u"ÿ" not in comments_history:
        return None

    a_list = comments_history.split(u'ÿ')[0:-1]
    second_list = [item.split(',')[0] for item in a_list if 'Not Exploitable' in item]
    name_and_project = second_list[0]
    d_list = name_and_project.split(" ")
    e_list = d_list[0:2]
    return " ".join(e_list)


def get_preset_list():
    """

    Returns:
        list of dict
    """

    @retry_when_unauthorized
    def execute():
        client, factory = get_client_and_factory(relative_web_interface_url=relative_web_interface_url)
        return client.service.GetPresetList(SessionID="0")

    response = execute()
    preset_list = response.PresetList
    return {
        "IsSuccesfull": response["IsSuccesfull"],
        "ErrorMessage": response["ErrorMessage"],
        "PresetList": [
            {
                "PresetName": item["PresetName"],
                "ID": item["ID"],
                "owningUser": item["owningUser"],
                "isUserAllowToUpdate": item["isUserAllowToUpdate"],
                "isUserAllowToDelete": item["isUserAllowToDelete"]
            } for item in preset_list["Preset"]
        ] if preset_list else None
    }


def get_projects_display_data():
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
    @retry_when_unauthorized
    def execute():
        client, factory = get_client_and_factory(relative_web_interface_url=relative_web_interface_url)
        return client.service.GetProjectsDisplayData(sessionID="0")

    response = execute()
    project_list = response.projectList
    return {
        "IsSuccesfull": response["IsSuccesfull"],
        "ErrorMessage": response["ErrorMessage"],
        "ProjectList": [
            {
                "Company": item["Company"],
                "Group": item["Group"],
                "IsPublic": item["IsPublic"],
                "LastScanDate": item["LastScanDate"],
                "Owner": item["Owner"],
                "Permission": item["Permission"],
                "Preset": item["Preset"],
                "ProjectName": item["ProjectName"],
                "ServiceProvider": item["ServiceProvider"],
                "TotalOsaScans": item["TotalOsaScans"],
                "TotalScans": item["TotalScans"],
                "projectID": item["projectID"],
            } for item in project_list.ProjectDisplayData
        ] if project_list else None
    }


def get_result_path(scan_id, path_id):
    """

    Args:
        scan_id (int):
        path_id (int):

    Returns:

    """

    @retry_when_unauthorized
    def execute():
        client, factory = get_client_and_factory(relative_web_interface_url=relative_web_interface_url)
        return client.service.GetResultPath(sessionId="0", scanId=scan_id, pathId=path_id)

    response = execute()
    item = response.Path
    return {
        "IsSuccesfull": response["IsSuccesfull"],
        "ErrorMessage": response["ErrorMessage"],
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
        }
    }


def get_results_for_scan(scan_id):
    """

    Args:
        scan_id (int):

    Returns:

    """

    @retry_when_unauthorized
    def execute():
        client, factory = get_client_and_factory(relative_web_interface_url=relative_web_interface_url)
        return client.service.GetResultsForScan(sessionID="0", scanId=scan_id)

    response = execute()
    scan_results_list = response.Results.CxWSSingleResultData
    return {
        "IsSuccesfull": response["IsSuccesfull"],
        "ErrorMessage": response["ErrorMessage"],
        "ScanResults": [
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
            } for item in scan_results_list
        ] if scan_results_list else None
    }


def get_server_license_data():
    """

    Returns:

    """

    @retry_when_unauthorized
    def execute():
        client, factory = get_client_and_factory(relative_web_interface_url=relative_web_interface_url)
        return client.service.GetServerLicenseData(sessionID="0")

    response = execute()
    supported_languages = response.SupportedLanguages
    return {
        "ExpirationDate": response["ExpirationDate"],
        "MaxConcurrentScans": response["MaxConcurrentScans"],
        "MaxLOC": response["MaxLOC"],
        "HID": response["HID"],
        "SupportedLanguages": [{
            "isSupported": item["isSupported"],
            "language": item["language"]
        } for item in supported_languages["SupportedLanguage"]
        ] if supported_languages else None,
        "MaxUsers": response["MaxUsers"],
        "CurrentUsers": response["CurrentUsers"],
        "MaxAuditUsers": response["MaxAuditUsers"],
        "CurrentAuditUsers": response["CurrentAuditUsers"],
        "IsOsaEnabled": response["IsOsaEnabled"],
        "OsaExpirationDate": response["OsaExpirationDate"],
        "Edition": response["Edition"],
        "ProjectsAllowed": response["ProjectsAllowed"],
        "CurrentProjectsCount": response["CurrentProjectsCount"]
    }


def get_server_license_summary():
    """

    Returns:

    """

    @retry_when_unauthorized
    def execute():
        client, factory = get_client_and_factory(relative_web_interface_url=relative_web_interface_url)
        return client.service.GetServerLicenseSummary(sessionID="0")

    response = execute()
    supported_languages = response.SupportedLanguages
    return {
        "ExpirationDate": response["ExpirationDate"],
        "MaxConcurrentScans": response["MaxConcurrentScans"],
        "MaxLOC": response["MaxLOC"],
        "HID": response["HID"],
        "SupportedLanguages": [{
            "isSupported": item["isSupported"],
            "language": item["language"]
        } for item in supported_languages["SupportedLanguage"]
        ] if supported_languages else None,
        "MaxUsers": response["MaxUsers"],
        "CurrentUsers": response["CurrentUsers"],
        "MaxAuditUsers": response["MaxAuditUsers"],
        "CurrentAuditUsers": response["CurrentAuditUsers"],
        "IsOsaEnabled": response["IsOsaEnabled"],
        "OsaExpirationDate": response["OsaExpirationDate"],
        "Edition": response["Edition"],
        "ProjectsAllowed": response["ProjectsAllowed"],
        "CurrentProjectsCount": response["CurrentProjectsCount"]
    }


def get_user_profile_data():
    """
    Notice: This method is not implemented by Portal SOAP API.
    The response IsSuccesfull is always False

    Returns:

    """
    @retry_when_unauthorized
    def execute():
        client, factory = get_client_and_factory(relative_web_interface_url=relative_web_interface_url)
        return client.service.GetUserProfileData(sessionID="0")

    response = execute()
    return {
        "IsSuccesfull": response["IsSuccesfull"],
        "ErrorMessage": response["ErrorMessage"],
        "ProfileData": response["ProfileData"],
    }


def get_version_number():
    """

    Returns:

    """

    @retry_when_unauthorized
    def execute():
        client, factory = get_client_and_factory(relative_web_interface_url=relative_web_interface_url)
        return client.service.GetVersionNumber()

    response = execute()
    return {
        "IsSuccesfull": response["IsSuccesfull"],
        "ErrorMessage": response["ErrorMessage"],
        "Version": response["Version"]
    }


def get_version_number_as_int():
    """
    8.9.0 -> 890
    9.2.0 -> 920
    9.3.0 -> 930
    9.4.0 -> 940
    9.4.1 -> 941
    Returns:
        int
    """
    version = get_version_number().get("Version").split(" ")[1]
    version = "".join(version.split("."))
    version = int(version)
    return version


def import_preset(imported_file_path):
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

    @retry_when_unauthorized
    def execute():
        client, factory = get_client_and_factory(relative_web_interface_url=relative_web_interface_url)
        return client.service.ImportPreset(sessionId="0", importedFile=imported_file)

    response = execute()
    return {
        "IsSuccesfull": response["IsSuccesfull"],
        "ErrorMessage": response["ErrorMessage"],
        "requestId": response["requestId"],
        "importQueryStatus": response["importQueryStatus"]
    }


def import_queries(imported_file_path):
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

    @retry_when_unauthorized
    def execute():
        client, factory = get_client_and_factory(relative_web_interface_url=relative_web_interface_url)
        return client.service.ImportQueries(sessionId="0", importedFile=imported_file)

    response = execute()
    return {
        "IsSuccesfull": response["IsSuccesfull"],
        "ErrorMessage": response["ErrorMessage"],
        "requestId": response["requestId"],
        "importQueryStatus": response["importQueryStatus"]
    }


def lock_scan(scan_id):
    """

    Args:
        scan_id (int):

    Returns:

    """

    @retry_when_unauthorized
    def execute():
        client, factory = get_client_and_factory(relative_web_interface_url=relative_web_interface_url)
        return client.service.LockScan(i_SessionID="0", i_ScanID=scan_id)

    response = execute()
    return {
        "IsSuccesfull": response["IsSuccesfull"],
        "ErrorMessage": response["ErrorMessage"],
    }


def unlock_scan(scan_id):
    """

        Args:
            scan_id (int):

        Returns:

        """

    @retry_when_unauthorized
    def execute():
        client, factory = get_client_and_factory(relative_web_interface_url=relative_web_interface_url)
        return client.service.UnlockScan(i_SessionID="0", i_ScanID=scan_id)

    response = execute()
    return {
        "IsSuccesfull": response["IsSuccesfull"],
        "ErrorMessage": response["ErrorMessage"],
    }
