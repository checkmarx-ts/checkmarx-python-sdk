from dataclasses import dataclass


@dataclass
class DastCliSettings:
    output: str = None
    retry: int = None
    retry_delay: int = None

    @classmethod
    def from_dict(cls, item: dict) -> "DastCliSettings":
        return cls(
            output=item.get("output"),
            retry=item.get("retry"),
            retry_delay=item.get("retryDelay"),
        )
