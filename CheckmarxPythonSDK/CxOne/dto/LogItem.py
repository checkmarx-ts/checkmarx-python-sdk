from dataclasses import dataclass


@dataclass
class LogItem:
    """

    Args:
        level (str): error, warn, info, debug
        msg (str):
        time (str):
        error (str):
        worker (str):
        raw_log (str):
    """
    level: str
    msg: str
    time: str
    error: str
    worker: str
    raw_log: str


def construct_log_item(item):
    return LogItem(
        level=item.get("level"),
        msg=item.get("msg"),
        time=item.get("time"),
        error=item.get("error"),
        worker=item.get("worker"),
        raw_log=item.get("rawLog")
    )
