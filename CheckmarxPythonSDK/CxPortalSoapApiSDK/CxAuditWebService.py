from os.path import exists
from CheckmarxPythonSDK.configuration import Configuration
from CheckmarxPythonSDK.CxPortalSoapApiSDK.config import construct_configuration
from .sudsClient import SudsClient


class CxAuditWebService(object):

    def __init__(self, configuration: Configuration = None):
        if configuration is None:
            configuration = construct_configuration()
            # configuration.is_sast_portal = True
        self.suds_client = SudsClient(
            relative_web_interface_url="/cxwebinterface/Audit/CxAuditWebService.asmx?wsdl",
            configuration=configuration,
        )

    def get_files_extensions(self) -> dict:
        response = self.suds_client.execute("GetFilesExtensions", sessionId="0")
        return {
            "IsSuccesfull": response.IsSuccesfull,
            "ErrorMessage": getattr(response, "ErrorMessage", None),
            "fileExtensionsSetList": [
                {
                    "Group": item.Group,
                    "IsPublic": item.IsPublic,
                    "Language": item.Language,
                    "OwningTeamId": item.OwningTeamId,
                    "OwningTeamName": getattr(item, "OwningTeamName", None),
                    "OwningUser": getattr(item, "OwningUser", None),
                    "Status": item.Status,
                    "Symbol": item.Symbol,
                    "Value": item.Value,
                }
                for item in (response.fileExtensionsSetList.FileExtension if response.fileExtensionsSetList else [])
            ],
        }

    def get_source_code_for_scan(self, scan_id: int) -> dict:
        response = self.suds_client.execute(
            "GetSourceCodeForScan", sessionID="0", scanId=scan_id
        )
        source_container = getattr(response, "sourceCodeContainer", None)
        return {
            "IsSuccesfull": response.IsSuccesfull,
            "ErrorMessage": getattr(response, "ErrorMessage", None),
            "sourceCodeContainer": (
                {
                    "FileName": source_container.FileName,
                    "ZippedFile": source_container.ZippedFile,
                }
                if source_container
                else None
            ),
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
            "QueryGroups": getattr(response, "QueryGroups", None),
        }

    def get_result_state_list(self) -> dict:
        response = self.suds_client.execute("GetResultStateList", sessionID="0")
        result_state_list = getattr(response, "ResultStateList", None)
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

    def update_result_state(
        self, scan_id: int, path_id: int, state: int, comment: str = ""
    ) -> dict:
        response = self.suds_client.execute(
            "UpdateResultState",
            sessionId="0",
            scanId=scan_id,
            pathId=path_id,
            state=state,
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
            scanID=scan_id,
            comment=comment,
        )
        return {
            "IsSuccesfull": response["IsSuccesfull"],
            "ErrorMessage": getattr(response, "ErrorMessage", None),
        }

    def get_project_scans(self, project_id: int) -> dict:
        response = self.suds_client.execute(
            "GetProjectScans", sessionId="0", projectId=project_id
        )
        scans_list = getattr(response, "ScansList", None)
        items = getattr(scans_list, "Scan", []) if scans_list else []
        return {
            "IsSuccesfull": response["IsSuccesfull"],
            "ErrorMessage": getattr(response, "ErrorMessage", None),
            "ScansList": [
                {
                    "ScanID": item.ScanID,
                    "StartDate": getattr(item, "StartDate", None),
                    "FinishDate": getattr(item, "FinishDate", None),
                    "ScanType": getattr(item, "ScanType", None),
                    "ScanStatus": getattr(item, "ScanStatus", None),
                }
                for item in (items if isinstance(items, list) else [items])
            ],
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

    def get_query_collection(self) -> dict:
        response = self.suds_client.execute("GetQueryCollection", sessionId="0")
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
            "GetQueryDescription", sessionId="0", cweId=cwe_id
        )
        return {
            "IsSuccesfull": response["IsSuccesfull"],
            "ErrorMessage": getattr(response, "ErrorMessage", None),
            "QueryDescription": getattr(response, "QueryDescription", None),
        }

    def get_query_description_by_query_id(self, query_id: int) -> dict:
        response = self.suds_client.execute(
            "GetQueryDescriptionByQueryId", sessionId="0", queryId=query_id
        )
        return {
            "IsSuccesfull": response.IsSuccesfull,
            "ErrorMessage": getattr(response, "ErrorMessage", None),
            "QueryDescription": response.QueryDescription,
        }

    def get_queries_categories(self) -> dict:
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

    def get_preset_list(self) -> dict:
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

    def get_path_comments_history(
        self, scan_id: int, path_id: int, label_type: str
    ) -> dict:
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

    def get_project_configuration(self, project_id: int) -> dict:
        response = self.suds_client.execute(
            "GetProjectConfiguration", sessionID="0", projectID=project_id
        )
        return {
            "IsSuccesfull": response["IsSuccesfull"],
            "ErrorMessage": getattr(response, "ErrorMessage", None),
            "ProjectConfig": getattr(response, "ProjectConfig", None),
        }

    def get_license_details(self) -> dict:
        response = self.suds_client.execute("GetLicenseDetails", sessionId="0")
        return {
            "IsSuccesfull": response["IsSuccesfull"],
            "ErrorMessage": getattr(response, "ErrorMessage", None),
            "LicenseDetails": getattr(response, "LicenseDetails", None),
        }

    def get_engine_configuration(self, configuration_id: int = 1) -> dict:
        response = self.suds_client.execute(
            "GetEngineConfiguration", sessionID="0", configurationId=configuration_id
        )
        return {
            "IsSuccesfull": response["IsSuccesfull"],
            "ErrorMessage": getattr(response, "ErrorMessage", None),
            "EngineConfig": getattr(response, "EngineConfig", None),
        }

    def get_hierarchy_group_tree(self) -> dict:
        response = self.suds_client.execute(
            "GetHierarchyGroupTree", sessionID="0"
        )
        return {
            "IsSuccesfull": response["IsSuccesfull"],
            "ErrorMessage": getattr(response, "ErrorMessage", None),
            "GroupTree": getattr(response, "GroupTree", None),
        }

    def get_ancestry_group_tree(self, team_id: str = "1") -> dict:
        response = self.suds_client.execute(
            "GetAncestryGroupTree", sessionID="0", pTeamID=team_id
        )
        return {
            "IsSuccesfull": response["IsSuccesfull"],
            "ErrorMessage": getattr(response, "ErrorMessage", None),
            "GroupTree": getattr(response, "GroupTree", None),
        }

    def keep_alive(self) -> dict:
        response = self.suds_client.execute("KeepAlive", sessionId="0")
        return {
            "IsSuccesfull": response["IsSuccesfull"],
            "ErrorMessage": getattr(response, "ErrorMessage", None),
        }

    def import_queries(self, imported_file_path: str) -> dict:
        if not exists(imported_file_path):
            print("Error, the imported file {} not exist".format(imported_file_path))
            return None
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

    def get_cache(self, scan_id: int = 0) -> dict:
        response = self.suds_client.execute("GetCache", sessionId="0", scanId=scan_id)
        return {
            "IsSuccesfull": response["IsSuccesfull"],
            "ErrorMessage": getattr(response, "ErrorMessage", None),
            "Cache": getattr(response, "Cache", None),
        }

    def upload_queries(self, query_groups: dict) -> dict:
        factory = self.suds_client.factory
        qgs = factory.ArrayOfCxWSQueryGroup(
            [
                factory.CxWSQueryGroup(
                    Name=qg["Name"],
                    Impacts=factory.ArrayOfInt(
                        [i for i in qg["Impacts"]] if qg["Impacts"] else qg["Impacts"]
                    ),
                    PackageId=qg["PackageId"],
                    Queries=factory.ArrayOfCxWSQuery(
                        [
                            factory.CxWSQuery(
                                Name=q["Name"],
                                QueryId=q["QueryId"],
                                Source=q["Source"],
                                Cwe=q["Cwe"],
                                IsExecutable=q["IsExecutable"],
                                IsEncrypted=q["IsEncrypted"],
                                Severity=q["Severity"],
                                PackageId=q["PackageId"],
                                Status=factory.QueryStatus(q["Status"]),
                                Type=factory.CxWSQueryType(q["Type"]),
                                Categories=factory.ArrayOfCxQueryCategory(
                                    [
                                        factory.CxQueryCategory(
                                            Id=c["Id"],
                                            CategoryName=c["CategoryName"],
                                            CategoryType=factory.CxCategoryType(
                                                Id=c["CategoryType"]["Id"],
                                                Name=c["CategoryType"]["Name"],
                                                Order=c["CategoryType"]["Order"],
                                            ),
                                        )
                                        for c in q["Categories"]
                                    ]
                                    if q["Categories"]
                                    else q["Categories"]
                                ),
                                CxDescriptionID=q["CxDescriptionID"],
                                QueryVersionCode=q["QueryVersionCode"],
                                EngineMetadata=q["EngineMetadata"],
                            )
                            for q in qg["Queries"]
                        ]
                        if qg["Queries"]
                        else qg["Queries"]
                    ),
                    IsReadOnly=qg["IsReadOnly"],
                    IsEncrypted=qg["IsEncrypted"],
                    Description=qg["Description"],
                    Language=qg["Language"],
                    LanguageName=qg["LanguageName"],
                    PackageTypeName=qg["PackageTypeName"],
                    ProjectId=qg["ProjectId"],
                    PackageType=factory.CxWSPackageTypeEnum(qg["PackageType"]),
                    PackageFullName=qg["PackageFullName"],
                    OwningTeam=qg["OwningTeam"],
                    Status=factory.QueryStatus(qg["Status"]),
                    # Mimicking CxAudit, we do not set LanguageStateHash
                    # LanguageStateHash=qg["LanguageStateHash"],
                    LanguageStateDate=qg["LanguageStateDate"],
                )
                for qg in query_groups
            ]
        )
        response = self.suds_client.execute(
            operation_name="UploadQueries", sessionId="0", queries=qgs
        )
        return {
            "IsSuccesfull": response.IsSuccesfull,
            "ErrorMessage": getattr(response, "ErrorMessage", None),
        }


def get_files_extensions() -> dict:
    return CxAuditWebService().get_files_extensions()


def get_source_code_for_scan(scan_id: int) -> dict:
    return CxAuditWebService().get_source_code_for_scan(scan_id=scan_id)


def upload_queries(query_groups: dict) -> dict:
    return CxAuditWebService().upload_queries(query_groups=query_groups)


def get_results(scan_id: int) -> dict:
    return CxAuditWebService().get_results(scan_id=scan_id)


def get_result_summary(scan_id: int) -> dict:
    return CxAuditWebService().get_result_summary(scan_id=scan_id)


def get_result_state_list() -> dict:
    return CxAuditWebService().get_result_state_list()


def update_result_state(
    scan_id: int, path_id: int, state: int, comment: str = ""
) -> dict:
    return CxAuditWebService().update_result_state(
        scan_id=scan_id, path_id=path_id, state=state, comment=comment
    )


def update_scan_comment(scan_id: int, comment: str) -> dict:
    return CxAuditWebService().update_scan_comment(scan_id=scan_id, comment=comment)


def get_project_scans(project_id: int) -> dict:
    return CxAuditWebService().get_project_scans(project_id=project_id)


def get_projects_with_scans() -> dict:
    return CxAuditWebService().get_projects_with_scans()


def get_query_collection() -> dict:
    return CxAuditWebService().get_query_collection()


def get_query_collection_for_language(
    project_type: str = "Regular", project_id: int = 0
) -> dict:
    return CxAuditWebService().get_query_collection_for_language(
        project_type=project_type, project_id=project_id
    )


def get_query_description(cwe_id: int) -> dict:
    return CxAuditWebService().get_query_description(cwe_id=cwe_id)


def get_query_description_by_query_id(query_id: int) -> dict:
    return CxAuditWebService().get_query_description_by_query_id(query_id=query_id)


def get_queries_categories() -> dict:
    return CxAuditWebService().get_queries_categories()


def get_preset_details(preset_id: int) -> dict:
    return CxAuditWebService().get_preset_details(preset_id=preset_id)


def get_preset_list() -> dict:
    return CxAuditWebService().get_preset_list()


def get_path_comments_history(scan_id: int, path_id: int, label_type: str) -> dict:
    return CxAuditWebService().get_path_comments_history(
        scan_id=scan_id, path_id=path_id, label_type=label_type
    )


def get_project_configuration(project_id: int) -> dict:
    return CxAuditWebService().get_project_configuration(project_id=project_id)


def get_license_details() -> dict:
    return CxAuditWebService().get_license_details()


def get_engine_configuration(configuration_id: int = 1) -> dict:
    return CxAuditWebService().get_engine_configuration(
        configuration_id=configuration_id
    )


def get_hierarchy_group_tree() -> dict:
    return CxAuditWebService().get_hierarchy_group_tree()


def get_ancestry_group_tree(team_id: str = "1") -> dict:
    return CxAuditWebService().get_ancestry_group_tree(team_id=team_id)


def keep_alive() -> dict:
    return CxAuditWebService().keep_alive()


def import_queries(imported_file_path: str) -> dict:
    return CxAuditWebService().import_queries(imported_file_path=imported_file_path)


def get_cache(scan_id: int = 0) -> dict:
    return CxAuditWebService().get_cache(scan_id=scan_id)
