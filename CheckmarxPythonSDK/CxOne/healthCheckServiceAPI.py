from CheckmarxPythonSDK.api_client import ApiClient
from CheckmarxPythonSDK.CxOne.config import construct_configuration
from .dto import SubCheck


class HealthCheckServiceAPI(object):

    def __init__(self, api_client: ApiClient = None):
        if api_client is None:
            configuration = construct_configuration()
            api_client = ApiClient(configuration=configuration)
        self.api_client = api_client
        self.base_url = (
            f"{self.api_client.configuration.server_base_url}/api/healthcheck"
        )

    def _parse_health(self, response) -> dict:
        data = response.json()
        return {
            "subChecks": [
                SubCheck.from_dict(item)
                for item in (data.get("subChecks") or [])
            ]
        }

    def get_health_of_the_database(self) -> dict:
        url = f"{self.base_url}/database"
        return self._parse_health(self.api_client.call_api(method="GET", url=url))

    def get_health_of_the_in_memory_db(self) -> dict:
        url = f"{self.base_url}/in-memory-db"
        return self._parse_health(self.api_client.call_api(method="GET", url=url))

    def get_health_of_the_message_queue(self) -> dict:
        url = f"{self.base_url}/message-queue"
        return self._parse_health(self.api_client.call_api(method="GET", url=url))

    def get_health_of_the_object_store_including_all_buckets(self) -> dict:
        url = f"{self.base_url}/object-store"
        return self._parse_health(self.api_client.call_api(method="GET", url=url))

    def get_health_of_the_logging(self) -> dict:
        url = f"{self.base_url}/logging"
        return self._parse_health(self.api_client.call_api(method="GET", url=url))

    def get_health_of_the_scan_flow(self) -> dict:
        url = f"{self.base_url}/scan-flow"
        return self._parse_health(self.api_client.call_api(method="GET", url=url))

    def get_health_of_the_sast_engines(self) -> dict:
        url = f"{self.base_url}/sast-engines"
        return self._parse_health(self.api_client.call_api(method="GET", url=url))


def get_health_of_the_database() -> dict:
    return HealthCheckServiceAPI().get_health_of_the_database()


def get_health_of_the_in_memory_db() -> dict:
    return HealthCheckServiceAPI().get_health_of_the_in_memory_db()


def get_health_of_the_message_queue() -> dict:
    return HealthCheckServiceAPI().get_health_of_the_message_queue()


def get_health_of_the_object_store_including_all_buckets() -> dict:
    return (
        HealthCheckServiceAPI().get_health_of_the_object_store_including_all_buckets()
    )


def get_health_of_the_logging() -> dict:
    return HealthCheckServiceAPI().get_health_of_the_logging()


def get_health_of_the_scan_flow() -> dict:
    return HealthCheckServiceAPI().get_health_of_the_scan_flow()


def get_health_of_the_sast_engines() -> dict:
    return HealthCheckServiceAPI().get_health_of_the_sast_engines()
