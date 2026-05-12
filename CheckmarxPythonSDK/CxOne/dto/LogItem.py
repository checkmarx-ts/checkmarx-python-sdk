from dataclasses import dataclass


@dataclass
class LogItem:
    level: str = None
    msg: str = None
    time: str = None
    error: str = None
    worker: str = None
    raw_log: str = None

    @classmethod
    def from_dict(cls, item: dict) -> "LogItem":
        return cls(
            level=item.get("level"),
            msg=item.get("msg"),
            time=item.get("time"),
            error=item.get("error"),
            worker=item.get("worker"),
            raw_log=item.get("rawLog"),
        )
