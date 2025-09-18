from dataclasses import dataclass


@dataclass
class WebError:
    code: int = None
    message: str = None
    data: dict = None


def construct_web_error(item):
    return WebError(
        code=item.get("code"),
        message=item.get("message"),
        data=item.get("data")
    )
