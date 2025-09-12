from CheckmarxPythonSDK.api_client import ApiClient
from CheckmarxPythonSDK.CxOne.config import construct_configuration
from .utilities import type_check
from .dto import (
    AuditEvents, construct_audit_events,
)

api_url = "/api/audit"


class AuditTrailAPI(object):

    def __init__(self, api_client: ApiClient = None):
        if api_client is None:
            configuration = construct_configuration()
            api_client = ApiClient(configuration=configuration)
        self.api_client = api_client

    def get_audit_events_for_tenant(
            self, date_from: str = None, date_to: str = None, offset: int = 0, limit: int = 200
    ) -> AuditEvents:
        """
        returns a list of audit events for the specified date range. - If no date range is specified, events from the
        last 365 days are returned. - The from_date cannot be more than 365 days in the past. - Events for the current
        day are returned inline. - Events for earlier dates are returned as downloadable links to daily JSON files.
        Args:
            date_from (str): Start date for the event filter in YYYY-MM-DD format. Cannot be more than 365 days in the
                             past.
            date_to (str): End date for the event filter in YYYY-MM-DD format. Must be the same or later than the
                            from_date.
            offset (int): The number of items to skip before starting to collect the result set
                        Default value : 0
            limit (int):  The number of items to return
                        Default value : 20

        Returns:
            `AuditEvents`
        """
        type_check(offset, int)
        type_check(limit, int)
        relative_url = api_url
        params = {"offset": offset, "limit": limit, "from": date_from, "to": date_to}
        response = self.api_client.get_request(relative_url=relative_url, params=params)
        item = response.json()
        return construct_audit_events(item)


def get_audit_events_for_tenant(date_from=None, date_to=None, offset=0, limit=200) -> AuditEvents:
    return AuditTrailAPI().get_audit_events_for_tenant(date_from=date_from, date_to=date_to, offset=offset, limit=limit)
