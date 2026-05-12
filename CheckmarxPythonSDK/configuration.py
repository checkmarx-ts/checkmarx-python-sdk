from dataclasses import dataclass
from typing import Union


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
    verify: Union[bool, str] = True
    cert: str = None  # path to client certificate
    proxy: str = None  # proxy URL, e.g. "http://proxy.example.com:8080"
    logging_level: str = "ERROR"  # DEBUG, INFO, WARNING, ERROR, CRITICAL
    max_retries: int = 3
    rate_limit_capacity: int = 20000  # Maximum number of requests
    rate_limit_period: int = 300  # Time period in seconds (5 minutes)
    rate_limit_refill_rate: float = None  # Tokens per second, auto-calculated if None
