
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
