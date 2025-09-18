from dataclasses import dataclass


@dataclass
class Error:
    message: str = None
    type: str = None
    code: int = None


def construct_error(item):
    return Error(
        message=item.get("message"),
        type=item.get("type"),
        code=item.get("code")
    )
