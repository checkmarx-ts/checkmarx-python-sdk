from CheckmarxPythonSDK.configuration import Configuration
from CheckmarxPythonSDK.CxPortalSoapApiSDK.config import construct_configuration
from .zeepClient import ZeepClient


class CxAuditWebService(object):

    def __init__(self, configuration: Configuration = None):
        if configuration is None:
            configuration = construct_configuration()
            # configuration.is_sast_portal = True
        self.zeep_client = ZeepClient(
                relative_web_interface_url="/cxwebinterface/Audit/CxAuditWebService.asmx?wsdl",
                configuration=configuration,
            )

    def get_files_extensions(self) -> dict:
        response = self.zeep_client.execute("GetFilesExtensions", sessionId="0")
        return {
            "IsSuccesfull": response.IsSuccesfull,
            "ErrorMessage": response.ErrorMessage,
            "fileExtensionsSetList": [
                {
                    "Group": item.Group,
                    "IsPublic": item.IsPublic,
                    "Language": item.Language,
                    "OwningTeamId": item.OwningTeamId,
                    "OwningTeamName": item.OwningTeamName,
                    "OwningUser": item.OwningUser,
                    "Status": item.Status,
                    "Symbol": item.Symbol,
                    "Value": item.Value,
                } for item in response.fileExtensionsSetList.FileExtension
            ]
        }

    def get_source_code_for_scan(self, scan_id: int) -> dict:
        response = self.zeep_client.execute("GetSourceCodeForScan", sessionID="0", scanId=scan_id)
        return {
            "IsSuccesfull": response.IsSuccesfull,
            "ErrorMessage": response.ErrorMessage,
            "sourceCodeContainer": {
                "FileName": response.sourceCodeContainer.FileName,
                "ZippedFile": response.sourceCodeContainer.ZippedFile,
            },
        }

    def upload_queries(self, query_groups: dict) -> dict:
        factory = self.zeep_client.factory
        qgs = factory.ArrayOfCxWSQueryGroup([
            factory.CxWSQueryGroup(
                Name=qg["Name"],
                Impacts=factory.ArrayOfInt([i for i in qg["Impacts"]] if qg["Impacts"] else qg["Impacts"]),
                PackageId=qg["PackageId"],
                Queries=factory.ArrayOfCxWSQuery([
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
                        Categories=factory.ArrayOfCxQueryCategory([
                            factory.CxQueryCategory(
                                Id=c["Id"],
                                CategoryName=c["CategoryName"],
                                CategoryType=factory.CxCategoryType(
                                    Id=c["CategoryType"]["Id"],
                                    Name=c["CategoryType"]["Name"],
                                    Order=c["CategoryType"]["Order"]
                                    )
                                ) for c in q["Categories"]
                            ] if q["Categories"] else q["Categories"]),
                        CxDescriptionID=q["CxDescriptionID"],
                        QueryVersionCode=q["QueryVersionCode"],
                        EngineMetadata=q["EngineMetadata"]
                        ) for q in qg["Queries"]
                    ] if qg["Queries"] else qg["Queries"]),
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
                LanguageStateDate=qg["LanguageStateDate"]
                ) for qg in query_groups
            ])
        response = self.zeep_client.execute(operation_name="UploadQueries", sessionId="0", queries=qgs)
        return {
            "IsSuccesfull": response.IsSuccesfull,
            "ErrorMessage": response.ErrorMessage
        }


def get_files_extensions() -> dict:
    return CxAuditWebService().get_files_extensions()


def get_source_code_for_scan(scan_id: int) -> dict:
    return CxAuditWebService().get_source_code_for_scan(scan_id=scan_id)


def upload_queries(query_groups: dict) -> dict:
    return CxAuditWebService().upload_queries(query_groups=query_groups)
