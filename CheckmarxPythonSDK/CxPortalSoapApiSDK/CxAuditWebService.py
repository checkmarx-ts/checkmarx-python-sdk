
from .zeepClient import get_client_and_factory, retry_when_unauthorized

relative_web_interface_url = "/cxwebinterface/Audit/CxAuditWebService.asmx?wsdl"


def get_source_code_for_scan(scan_id):

    @retry_when_unauthorized
    def execute():
        client, factory = get_client_and_factory(relative_web_interface_url=relative_web_interface_url)
        return client.service.GetSourceCodeForScan(sessionID="0", scanId=scan_id)

    response = execute()
    return response
