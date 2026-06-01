from dataclasses import dataclass


@dataclass
class DastAuthSettings:
    verification_url: str = None
    logged_in_regex: str = None
    login_page_wait: int = None

    @classmethod
    def from_dict(cls, item: dict) -> "DastAuthSettings":
        return cls(
            verification_url=item.get("verificationURL"),
            logged_in_regex=item.get("loggedInRegex"),
            login_page_wait=item.get("loginPageWait"),
        )
