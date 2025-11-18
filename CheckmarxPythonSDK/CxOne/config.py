# encoding: utf-8
from CheckmarxPythonSDK.utilities.configUtility import get_config
from CheckmarxPythonSDK.configuration import Configuration


def construct_configuration() -> Configuration:
    config_default = {
        "access_control_url": "https://iam.checkmarx.net",
        "server": "https://ast.checkmarx.net",
        "tenant_name": None,
        "grant_type": "refresh_token",
        "client_id": "ast-app",
        "client_secret": None,
        "username": None,
        "password": None,
        "refresh_token": None,
        "timeout": 60,
        "verify": True,
        "cert": None,
        "proxy": None,
    }
    config = get_config(config_default=config_default, section="CxOne", prefix="cxone_")
    return Configuration(
                server_base_url=config.get("server"),
                iam_base_url=config.get("access_control_url"),
                token_url=(
                    f"{config.get('access_control_url')}/auth/realms"
                    f"/{config.get('tenant_name')}/protocol/openid-connect/token"
                ),
                tenant_name=config.get("tenant_name"),
                grant_type=config.get("grant_type"),
                client_id=config.get("client_id"),
                client_secret=config.get("client_secret"),
                api_key=config.get("refresh_token"),
                timeout=int(config.get("timeout")),
                verify=config.get("verify"),
                cert=config.get("cert"),
                proxies={
                    "http": config.get("proxy"),
                    "https": config.get("proxy"),
                }
            )
