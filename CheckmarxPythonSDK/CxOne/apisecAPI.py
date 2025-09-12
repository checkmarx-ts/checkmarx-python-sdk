from CheckmarxPythonSDK.api_client import ApiClient
from CheckmarxPythonSDK.CxOne.config import construct_configuration


class ApiSecAPI(object):

    def __init__(self, api_client: ApiClient = None):
        if api_client is None:
            configuration = construct_configuration()
            api_client = ApiClient(configuration=configuration)
        self.api_client = api_client

    def get_scan_apisec_risk_overview(self, scan_id: str) -> dict:
        relative_url = f"/api/apisec/static/api/scan/{scan_id}/risks-overview"
        response = self.api_client.get_request(relative_url=relative_url)
        return response.json()


def get_scan_apisec_risk_overview(scan_id: str) -> dict:
    return ApiSecAPI().get_scan_apisec_risk_overview(scan_id)
