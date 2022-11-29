from .httpRequests import get_request
from .dto import SubCheck


def __construct_health_check(response):
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


def get_health_of_the_database():
    relative_url = "/api/healthcheck/database"
    response = get_request(relative_url=relative_url)
    return __construct_health_check(response)


def get_health_of_the_in_memory_db():
    relative_url = "/api/healthcheck/in-memory-db"
    response = get_request(relative_url=relative_url)
    return __construct_health_check(response)


def get_health_of_the_message_queue():
    relative_url = "/api/healthcheck/message-queue"
    response = get_request(relative_url=relative_url)
    return __construct_health_check(response)


def get_health_of_the_object_stroe_including_all_buckets():
    relative_url = "/api/healthcheck/object-store"
    response = get_request(relative_url=relative_url)
    return __construct_health_check(response)


def get_health_of_the_logging():
    relative_url = "/api/healthcheck/logging"
    response = get_request(relative_url=relative_url)
    return __construct_health_check(response)


def get_health_of_the_scan_flow():
    relative_url = "/api/healthcheck/scan-flow"
    response = get_request(relative_url=relative_url)
    return __construct_health_check(response)


def get_health_of_the_sast_engines():
    relative_url = "/api/healthcheck/sast-engines"
    response = get_request(relative_url=relative_url)
    return __construct_health_check(response)
