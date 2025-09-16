from CheckmarxPythonSDK.configuration import Configuration
from CheckmarxPythonSDK.utilities.configUtility import get_config


def construct_configuration() -> Configuration:
    config_default = {
        "access_control_url": "https://platform.checkmarx.net",
        "server": "https://api-sca.checkmarx.net",
        "account": None,
        "username": None,
        "password": None,
        "scope": "sca_api access_control_api",
        "timeout": 60,
        "verify": True,
        "cert": None,
        "proxy": None,
    }
    config = get_config(config_default=config_default, section="CxSCA", prefix="cxsca_")
    return Configuration(
                server_base_url=config.get("server"),
                iam_base_url=config.get("access_control_url"),
                token_url=f"{config.get('access_control_url')}/identity/connect/token",
                tenant_name=config.get("account"),
                username=config.get("username"),
                password=config.get("password"),
                scope=config.get("scope"),
                timeout=config.get("timeout"),
                verify=config.get("verify"),
                cert=config.get("cert"),
                proxies={
                    "http": config.get("proxy"),
                    "https": config.get("proxy"),
                }
            )
