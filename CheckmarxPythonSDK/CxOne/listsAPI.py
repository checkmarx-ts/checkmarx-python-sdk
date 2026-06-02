from CheckmarxPythonSDK.api_client import ApiClient
from CheckmarxPythonSDK.CxOne.config import construct_configuration
from typing import List


class ListsAPI(object):

    def __init__(self, api_client: ApiClient = None):
        if api_client is None:
            configuration = construct_configuration()
            api_client = ApiClient(configuration=configuration)
        self.api_client = api_client
        self.base_url = (
            f"{self.api_client.configuration.server_base_url}/api/lists"
        )

    def get_severities(self) -> List[str]:
        """
        Get the list of severity values.

        Returns:
            list of str (e.g. CRITICAL, HIGH, MEDIUM, LOW, INFO)
        """
        url = f"{self.base_url}/severities"
        response = self.api_client.call_api(method="GET", url=url)
        return response.json()

    def get_states(self) -> List[str]:
        """
        Get the list of state values.

        Returns:
            list of str (e.g. TO_VERIFY, CONFIRMED, URGENT)
        """
        url = f"{self.base_url}/states"
        response = self.api_client.call_api(method="GET", url=url)
        return response.json()

    def get_statuses(self) -> List[str]:
        """
        Get the list of status values.

        Returns:
            list of str (e.g. NEW, RECURRENT, FIXED)
        """
        url = f"{self.base_url}/statuses"
        response = self.api_client.call_api(method="GET", url=url)
        return response.json()


# ---- Module-level convenience functions ----

def get_severities() -> List[str]:
    return ListsAPI().get_severities()


def get_states() -> List[str]:
    return ListsAPI().get_states()


def get_statuses() -> List[str]:
    return ListsAPI().get_statuses()
