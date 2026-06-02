from CheckmarxPythonSDK.api_client import ApiClient
from CheckmarxPythonSDK.CxOne.config import construct_configuration


class StaticCorrelatorAPI(object):

    def __init__(self, api_client: ApiClient = None):
        if api_client is None:
            configuration = construct_configuration()
            api_client = ApiClient(configuration=configuration)
        self.api_client = api_client
        self.base_url = (
            f"{self.api_client.configuration.server_base_url}"
            f"/api/apisec/correlator"
        )

    def update_risk(
        self,
        scan_id: str,
        method: str,
        similarity_id: str,
        url: str,
        severity: str = None,
        state: str = None,
    ) -> dict:
        """
        Update risk state and/or severity.

        Args:
            scan_id (str): Scan ID (path param)
            method (str): HTTP method
            similarity_id (str): The similarity identifier
            url (str): The target URL
            severity (str): Severity value (optional)
            state (str): Risk state (optional)

        Returns:
            dict with message
        """
        url_path = f"{self.base_url}/api/risk/{scan_id}"
        body = {
            "method": method,
            "similarity_id": similarity_id,
            "url": url,
        }
        if severity:
            body["severity"] = severity
        if state:
            body["state"] = state
        response = self.api_client.call_api(
            method="PUT", url=url_path, json=body
        )
        return response.json()


# ---- Module-level convenience function ----

def update_risk(
    scan_id: str,
    method: str,
    similarity_id: str,
    url: str,
    severity: str = None,
    state: str = None,
) -> dict:
    return StaticCorrelatorAPI().update_risk(
        scan_id=scan_id, method=method, similarity_id=similarity_id,
        url=url, severity=severity, state=state,
    )
