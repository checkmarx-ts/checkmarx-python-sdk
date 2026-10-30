from dataclasses import dataclass
from typing import Optional


@dataclass
class DastAuthSessionCredentials:
    """The `Credentials` field on GET /authSession/{envId} (method=CREDENTIALS).

    Confirmed live: camelCase, unlike most of the rest of the auth
    session request/response surface (PascalCase).
    """
    user_name: Optional[str] = None
    password: Optional[str] = None
    login_page_url: Optional[str] = None

    @classmethod
    def from_dict(cls, item: dict) -> "DastAuthSessionCredentials":
        return cls(
            user_name=item.get("userName"),
            password=item.get("password"),
            login_page_url=item.get("loginPageURL"),
        )
