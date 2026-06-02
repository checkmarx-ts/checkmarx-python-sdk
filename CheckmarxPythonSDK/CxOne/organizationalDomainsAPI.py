from CheckmarxPythonSDK.api_client import ApiClient
from CheckmarxPythonSDK.CxOne.config import construct_configuration
from CheckmarxPythonSDK.utilities.compat import NO_CONTENT


class OrganizationalDomainsAPI(object):

    def __init__(self, api_client: ApiClient = None):
        if api_client is None:
            configuration = construct_configuration()
            api_client = ApiClient(configuration=configuration)
        self.api_client = api_client
        self.base_url = (
            f"{self.api_client.configuration.server_base_url}"
            f"/api/organizational-domains"
        )

    def list_organizational_domains(
        self,
        search: str = None,
        offset: int = 1,
        limit: int = 10,
    ) -> dict:
        """
        List organizational domains for the tenant.

        Args:
            search (str): Optional case-insensitive contains match
            offset (int): 1-based page offset. Default: 1
            limit (int): Items per page (1-100). Default: 10

        Returns:
            dict with items and total
        """
        url = f"{self.base_url}"
        params = {"search": search, "offset": offset, "limit": limit}
        response = self.api_client.call_api(
            method="GET", url=url, params=params
        )
        return response.json()

    def add_organizational_domains(self, domains: str) -> dict:
        """
        Add organizational domains to the tenant.

        Args:
            domains (str): Semicolon-separated domain names,
                e.g. "example.com;example.org"

        Returns:
            dict with added and invalid arrays
        """
        url = f"{self.base_url}"
        response = self.api_client.call_api(
            method="POST", url=url, json={"domains": domains}
        )
        return response.json()

    def delete_organizational_domain(self, id: str) -> bool:
        """
        Remove an organizational domain.

        Args:
            id (str): Domain ID (uuid)

        Returns:
            bool
        """
        url = f"{self.base_url}/{id}"
        response = self.api_client.call_api(method="DELETE", url=url)
        return response.status_code == NO_CONTENT


# ---- Module-level convenience functions ----

def list_organizational_domains(
    search: str = None,
    offset: int = 1,
    limit: int = 10,
) -> dict:
    return OrganizationalDomainsAPI().list_organizational_domains(
        search=search, offset=offset, limit=limit,
    )


def add_organizational_domains(domains: str) -> dict:
    return OrganizationalDomainsAPI().add_organizational_domains(
        domains=domains
    )


def delete_organizational_domain(id: str) -> bool:
    return OrganizationalDomainsAPI().delete_organizational_domain(id=id)
