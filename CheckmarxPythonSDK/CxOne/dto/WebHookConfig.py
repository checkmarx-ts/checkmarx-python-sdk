from dataclasses import dataclass


@dataclass
class WebHookConfig:
    """
    Attributes:
       contentType (str):  Webhooks payload content type
       insecureSsl (bool): Enable SSL verification
       url (str): Payload URL
       secret (str): Post request attached secret
    """

    contentType: str = None
    insecureSsl: bool = None
    url: str = None
    secret: str = None

    @classmethod
    def from_dict(cls, item: dict) -> "WebHookConfig":
        return cls(
            contentType=item.get("contentType"),
            insecureSsl=item.get("insecureSsl"),
            url=item.get("url"),
            secret=item.get("secret"),
        )
