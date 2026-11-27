from typing import List

from CheckmarxPythonSDK.api_client import ApiClient
from CheckmarxPythonSDK.CxOne.config import construct_configuration
from CheckmarxPythonSDK.CxOne.dto import ScmCoverage


class DiscoveryAPI(object):

    def __init__(self, api_client: ApiClient = None):
        if api_client is None:
            configuration = construct_configuration()
            api_client = ApiClient(configuration=configuration)
        self.api_client = api_client
        self.base_url = (
            f"{self.api_client.configuration.server_base_url}/api/discovery"
        )

    def get_orgs_coverage(self) -> List[ScmCoverage]:
        """
        Repository import coverage per SCM instance and organization
        (GET /api/discovery/v2/orgs/coverage): how many repos each org has
        and how many are imported as Checkmarx One projects.

        Returns:
            List[ScmCoverage]
        """
        url = f"{self.base_url}/v2/orgs/coverage"
        response = self.api_client.call_api(method="GET", url=url)
        return [ScmCoverage.from_dict(item) for item in response.json()]


def get_orgs_coverage() -> List[ScmCoverage]:
    return DiscoveryAPI().get_orgs_coverage()
