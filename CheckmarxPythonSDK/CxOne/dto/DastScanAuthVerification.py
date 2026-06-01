from dataclasses import dataclass
from typing import List
from .DastPollHeader import DastPollHeader


@dataclass
class DastScanAuthVerification:
    logged_in_regex: str = None
    logged_out_regex: str = None
    method: str = None
    poll_additional_headers: List[DastPollHeader] = None
    poll_frequency: int = None
    poll_post_data: str = None
    poll_url: str = None
    poll_units: str = None

    @classmethod
    def from_dict(cls, item: dict) -> "DastScanAuthVerification":
        return cls(
            logged_in_regex=item.get("LoggedInRegex"),
            logged_out_regex=item.get("LoggedOutRegex"),
            method=item.get("Method"),
            poll_additional_headers=[
                DastPollHeader.from_dict(h) for h in (item.get("PollAdditionalHeaders") or [])
            ],
            poll_frequency=item.get("PollFrequency"),
            poll_post_data=item.get("PollPostData"),
            poll_url=item.get("PollURL"),
            poll_units=item.get("PollUnits"),
        )
