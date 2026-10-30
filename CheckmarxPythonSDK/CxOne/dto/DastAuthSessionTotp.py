from dataclasses import dataclass, asdict
from typing import Optional


@dataclass
class DastAuthSessionTotp:
    """Request-side `TOTP` object for PUT /authSession/credentials."""
    secret_key: Optional[str] = None
    otp_length: Optional[int] = None
    period: Optional[int] = None

    def to_dict(self) -> dict:
        raw = {
            "SecretKey": self.secret_key,
            "OTPLength": self.otp_length,
            "Period": self.period,
        }
        return {k: v for k, v in raw.items() if v is not None}
