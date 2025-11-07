class GlobalRequestResult:
    def __init__(self, failed_requests, success_requests):
        self.failedRequests = failed_requests
        self.successRequests = success_requests

    def __str__(self):
        return f"GlobalRequestResult(" \
               f"failedRequests={self.failedRequests} " \
               f"successRequests={self.successRequests} " \
               f")"

    def to_dict(self):
        return {
            "failedRequests": self.failedRequests,
            "successRequests": self.successRequests,
        }


def construct_global_request_result(item):
    return GlobalRequestResult(
        failed_requests=item.get("failedRequests"),
        success_requests=item.get("successRequests"),
    )
