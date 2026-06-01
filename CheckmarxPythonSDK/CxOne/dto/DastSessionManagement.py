from dataclasses import dataclass


@dataclass
class DastSessionManagement:
    method: str = None
    # Parameters shape varies by method (e.g. {"cookie": "..."} for cookie
    # method, header pairs for headers method). Left raw until enough
    # variants are observed to model cleanly.
    parameters: dict = None

    @classmethod
    def from_dict(cls, item: dict) -> "DastSessionManagement":
        return cls(
            method=item.get("Method"),
            parameters=item.get("Parameters"),
        )
