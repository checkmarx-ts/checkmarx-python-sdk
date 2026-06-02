from CheckmarxPythonSDK.api_client import ApiClient
from CheckmarxPythonSDK.CxOne.config import construct_configuration


class AuditEventProcessorAPI(object):

    def __init__(self, api_client: ApiClient = None):
        if api_client is None:
            configuration = construct_configuration()
            api_client = ApiClient(configuration=configuration)
        self.api_client = api_client
        self.base_url = (
            f"{self.api_client.configuration.server_base_url}"
            f"/api/audit-events"
        )

    def get_audit_events(
        self,
        offset: int = 0,
        limit: int = 100,
        start_date: str = None,
        end_date: str = None,
    ) -> dict:
        """
        Get a list of audit events.

        Args:
            offset (int): Items to skip. Default: 0
            limit (int): Max results (0-1000). Default: 100
            start_date (str): Earliest event date (RFC3339)
            end_date (str): Latest event date (RFC3339)

        Returns:
            dict with filteredTotalCount, _links, events
        """
        url = f"{self.base_url}/"
        params = {
            "offset": offset,
            "limit": limit,
            "startDate": start_date,
            "endDate": end_date,
        }
        response = self.api_client.call_api(
            method="GET", url=url, params=params
        )
        return response.json()


# ---- Module-level convenience function ----

def get_audit_events(
    offset: int = 0,
    limit: int = 100,
    start_date: str = None,
    end_date: str = None,
) -> dict:
    return AuditEventProcessorAPI().get_audit_events(
        offset=offset, limit=limit, start_date=start_date, end_date=end_date,
    )
