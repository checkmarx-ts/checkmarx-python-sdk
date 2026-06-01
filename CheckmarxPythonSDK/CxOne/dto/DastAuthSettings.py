from dataclasses import dataclass
from typing import List
from .DastTotpField import DastTotpField


@dataclass
class DastAuthSettings:
    """Request-side authSettings for POST /api/dast/scans/environment."""
    # NOTE: the latest doc spells this "verificationUrl" (lowercase rl);
    # an earlier revision had "verificationURL". Trusting the newer one.
    verification_url: str = None
    logged_in_regex: str = None
    login_page_wait: int = None
    include_paths: List[str] = None
    logged_out_regex: str = None
    poll_post_data: str = None
    totp_field: DastTotpField = None
    # Documented as `string` (not array) on the request side.
    poll_additional_headers: str = None

    def to_dict(self) -> dict:
        raw = {
            "verificationUrl": self.verification_url,
            "loggedInRegex": self.logged_in_regex,
            "loginPageWait": self.login_page_wait,
            "includePaths": self.include_paths,
            "loggedOutRegex": self.logged_out_regex,
            "pollPostData": self.poll_post_data,
            "totpField": self.totp_field.to_dict() if self.totp_field else None,
            "pollAdditionalHeaders": self.poll_additional_headers,
        }
        return {k: v for k, v in raw.items() if v is not None}
