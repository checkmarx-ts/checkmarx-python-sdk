from dataclasses import dataclass


@dataclass
class Configuration:
    server_base_url: str = None
    iam_base_url: str = None
    token_url: str = None
    tenant_name: str = None
    username: str = None
    password: str = None
    grant_type: str = None
    scope: str = None
    client_id: str = None
    client_secret: str = None
    api_key: str = None
    timeout: int = 60
    verify_ssl_cert: bool = False
    cert: str = None  # path to client certificate
    proxies: dict = None
    debug_mode: bool = False
    max_retries: int = 3
