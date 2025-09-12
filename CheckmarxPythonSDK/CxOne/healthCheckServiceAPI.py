from CheckmarxPythonSDK.api_client import ApiClient
from CheckmarxPythonSDK.CxOne.config import construct_configuration
from .dto import SubCheck

api_url = "/api/healthcheck"


def construct_health_check(response):
    response = response.json()
    return {
        "subChecks": [
            SubCheck(
                name=item.get("name"),
                success=item.get("success"),
                errors=item.get("errors")
            )
            for item in response.get("subChecks") or []]
    }


class HealthCheckServiceAPI(object):

    def __init__(self, api_client: ApiClient = None):
        if api_client is None:
            configuration = construct_configuration()
            api_client = ApiClient(configuration=configuration)
        self.api_client = api_client

    def get_health_of_the_database(self) -> dict:
        relative_url = api_url + "/database"
        response = self.api_client.get_request(relative_url=relative_url)
        return construct_health_check(response)

    def get_health_of_the_in_memory_db(self) -> dict:
        relative_url = api_url + "/in-memory-db"
        response = self.api_client.get_request(relative_url=relative_url)
        return construct_health_check(response)

    def get_health_of_the_message_queue(self) -> dict:
        relative_url = api_url + "/message-queue"
        response = self.api_client.get_request(relative_url=relative_url)
        return construct_health_check(response)

    def get_health_of_the_object_store_including_all_buckets(self) -> dict:
        relative_url = api_url + "/object-store"
        response = self.api_client.get_request(relative_url=relative_url)
        return construct_health_check(response)

    def get_health_of_the_logging(self) -> dict:
        relative_url = api_url + "/logging"
        response = self.api_client.get_request(relative_url=relative_url)
        return construct_health_check(response)

    def get_health_of_the_scan_flow(self) -> dict:
        relative_url = api_url + "/scan-flow"
        response = self.api_client.get_request(relative_url=relative_url)
        return construct_health_check(response)

    def get_health_of_the_sast_engines(self) -> dict:
        relative_url = api_url + "/sast-engines"
        response = self.api_client.get_request(relative_url=relative_url)
        return construct_health_check(response)


def get_health_of_the_database() -> dict:
    return HealthCheckServiceAPI().get_health_of_the_database()


def get_health_of_the_in_memory_db() -> dict:
    return HealthCheckServiceAPI().get_health_of_the_in_memory_db()


def get_health_of_the_message_queue() -> dict:
    return HealthCheckServiceAPI().get_health_of_the_message_queue()


def get_health_of_the_object_store_including_all_buckets() -> dict:
    return HealthCheckServiceAPI().get_health_of_the_object_store_including_all_buckets()


def get_health_of_the_logging() -> dict:
    return HealthCheckServiceAPI().get_health_of_the_logging()


def get_health_of_the_scan_flow() -> dict:
    return HealthCheckServiceAPI().get_health_of_the_scan_flow()


def get_health_of_the_sast_engines() -> dict:
    return HealthCheckServiceAPI().get_health_of_the_sast_engines()
