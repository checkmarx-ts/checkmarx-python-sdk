from dataclasses import dataclass


@dataclass
class WebError:
    code: int = None
    message: str = None
    data: dict = None
