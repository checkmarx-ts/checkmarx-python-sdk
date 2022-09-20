
from .zeepClient import get_client_and_factory, retry_when_unauthorized

relative_web_interface_url = "/cxwebinterface/Audit/CxAuditWebService.asmx?wsdl"


def get_files_extensions():

    @retry_when_unauthorized
    def execute():
        client, factory = get_client_and_factory(relative_web_interface_url=relative_web_interface_url)
        return client.service.GetFilesExtensions(sessionId="0")

    response = execute()
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


def get_source_code_for_scan(scan_id):

    @retry_when_unauthorized
    def execute():
        client, factory = get_client_and_factory(relative_web_interface_url=relative_web_interface_url)
        return client.service.GetSourceCodeForScan(sessionID="0", scanId=scan_id)

    response = execute()
    return {
        "IsSuccesfull": response.IsSuccesfull,
        "ErrorMessage": response.ErrorMessage,
        "sourceCodeContainer": {
            "FileName": response.sourceCodeContainer.FileName,
            "ZippedFile": response.sourceCodeContainer.ZippedFile,
        },
    }


def upload_queries(query_groups):

    @retry_when_unauthorized
    def execute():
        client, factory = get_client_and_factory(relative_web_interface_url=relative_web_interface_url)
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

        return client.service.UploadQueries(sessionId="0", queries=qgs)

    response = execute()

    return {
        "IsSuccesfull": response.IsSuccesfull,
        "ErrorMessage": response.ErrorMessage
    }
