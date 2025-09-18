from dataclasses import dataclass


@dataclass
class AsyncRequestResponse:
    id: str = None

    def to_dict(self):
        return {
            "id": self.id
        }


def construct_async_request_response(item):
    return AsyncRequestResponse(
        id=item.get("id")
    )
