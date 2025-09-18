from dataclasses import dataclass


@dataclass
class WebHookConfig:
    """
    Attributes:
       content_type (str):  Webhooks payload content type
       insecure_ssl (bool): Enable SSL verification
       url (str): Payload URL
       secret (str): Post request attached secret
    """
    content_type: str = None
    insecure_ssl: bool = None
    url: str = None
    secret: str = None

    def to_dict(self):
        return {
            "contentType": self.content_type,
            "insecureSsl": self.insecure_ssl,
            "url": self.url,
            "secret": self.secret
        }


def construct_web_hook_config(item):
    return WebHookConfig(
        content_type=item.get("contentType"),
        insecure_ssl=item.get("insecureSsl"),
        url=item.get("url"),
        secret=item.get("secret")
    )
