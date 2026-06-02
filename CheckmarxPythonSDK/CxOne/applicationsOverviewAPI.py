from CheckmarxPythonSDK.api_client import ApiClient
from CheckmarxPythonSDK.CxOne.config import construct_configuration
from typing import List


class ApplicationsOverviewAPI(object):

    def __init__(self, api_client: ApiClient = None):
        if api_client is None:
            configuration = construct_configuration()
            api_client = ApiClient(configuration=configuration)
        self.api_client = api_client
        self.base_url = (
            f"{self.api_client.configuration.server_base_url}"
            f"/api/applications-overview"
        )

    def get_applications_overview(
        self,
        offset: int = 0,
        limit: int = 10,
        name: List[str] = None,
        risk_level: List[str] = None,
        empty_tags: bool = False,
        criticality: List[str] = None,
        sort: List[str] = None,
    ) -> dict:
        """
        Get an overview of all applications.

        Args:
            offset (int): Request offset. Default: 0
            limit (int): Items per page (max 100). Default: 10
            name (List[str]): Filter by application name
            risk_level (List[str]): Info, Low, Medium, High, Critical
            empty_tags (bool): Filter by empty tags. Default: False
            criticality (List[str]): Low, Medium, High, Critical, None
            sort (List[str]): name, criticality, num-of-projects, risk-level

        Returns:
            dict with applications array
        """
        url = f"{self.base_url}"
        params = {
            "offset": offset,
            "limit": limit,
            "name": name,
            "risk-level": risk_level,
            "empty-tags": empty_tags,
            "criticality": criticality,
            "sort": sort,
        }
        response = self.api_client.call_api(
            method="GET", url=url, params=params
        )
        return response.json()

    def get_applications_overview_aggregate(
        self, group_by_field: List[str]
    ) -> dict:
        """
        Get application overview counters.

        Args:
            group_by_field (List[str]): Fields to group by.
                Values: criticality, risk_level

        Returns:
            dict with applicationsCounters array
        """
        url = f"{self.base_url}/aggregate"
        params = {"group-by-field": group_by_field}
        response = self.api_client.call_api(
            method="GET", url=url, params=params
        )
        return response.json()

    def get_applications_overview_count(self) -> int:
        """
        Get the count of application overviews.

        Returns:
            int
        """
        url = f"{self.base_url}/applications-overview-count"
        response = self.api_client.call_api(method="GET", url=url)
        return response.json()


# ---- Module-level convenience functions ----

def get_applications_overview(
    offset: int = 0,
    limit: int = 10,
    name: List[str] = None,
    risk_level: List[str] = None,
    empty_tags: bool = False,
    criticality: List[str] = None,
    sort: List[str] = None,
) -> dict:
    return ApplicationsOverviewAPI().get_applications_overview(
        offset=offset, limit=limit, name=name, risk_level=risk_level,
        empty_tags=empty_tags, criticality=criticality, sort=sort,
    )


def get_applications_overview_aggregate(
    group_by_field: List[str]
) -> dict:
    return ApplicationsOverviewAPI().get_applications_overview_aggregate(
        group_by_field=group_by_field
    )


def get_applications_overview_count() -> int:
    return ApplicationsOverviewAPI().get_applications_overview_count()
