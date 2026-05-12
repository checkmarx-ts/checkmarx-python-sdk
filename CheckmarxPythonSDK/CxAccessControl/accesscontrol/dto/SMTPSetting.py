from dataclasses import dataclass
from typing import Optional


@dataclass
class SMTPSetting:
    id: Optional[int] = None
    host: Optional[str] = None
    port: Optional[int] = None
    encryption_type: Optional[str] = None
    from_address: Optional[str] = None
    use_default_credentials: Optional[bool] = None
    username: Optional[str] = None

    @classmethod
    def from_dict(cls, item: dict) -> "SMTPSetting":
        return cls(
            id=item.get("id"),
            host=item.get("host"),
            port=item.get("port"),
            encryption_type=item.get("encryptionType"),
            from_address=item.get("fromAddress"),
            use_default_credentials=item.get("useDefaultCredentials"),
            username=item.get("username"),
        )
