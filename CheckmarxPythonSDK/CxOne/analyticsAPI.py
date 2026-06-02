from CheckmarxPythonSDK.api_client import ApiClient
from CheckmarxPythonSDK.CxOne.config import construct_configuration
from typing import List


class AnalyticsAPI(object):

    def __init__(self, api_client: ApiClient = None):
        if api_client is None:
            configuration = construct_configuration()
            api_client = ApiClient(configuration=configuration)
        self.api_client = api_client
        self.base_url = (
            f"{self.api_client.configuration.server_base_url}"
            f"/api/data_analytics"
        )

    def query_kpi(self, body: dict) -> dict:
        """
        Query an analytics KPI.

        Args:
            body (dict): Request body with at minimum a 'kpi' field.
                Common optional fields: projects, applications, scanners,
                states, severities, status, startDate, endDate, limit,
                offset, timezone, etc.

        Returns:
            dict — response shape depends on the kpi value selected
        """
        url = f"{self.base_url}/analyticsAPI/v1"
        response = self.api_client.call_api(
            method="POST", url=url, json=body
        )
        return response.json()


# ---- Module-level convenience function ----

def query_kpi(body: dict) -> dict:
    return AnalyticsAPI().query_kpi(body=body)
