from CheckmarxPythonSDK.configuration import Configuration
from CheckmarxPythonSDK.utilities.configUtility import get_config


def construct_configuration() -> Configuration:
    config_default = {
        "base_url": "http://localhost",
        "reporting_client_url": "http://localhost:5001",
        "username": "Admin",
        "password": "password",
        "grant_type": "password",
        "scope": "reporting_api",
        "client_id": "reporting_service_api",
        "client_secret": "014DF517-39D1-4453-B7B3-9930C563627C",
        "timeout": 60,
        "verify": True,
        "cert": None,
        "proxy": None,
    }
    config = get_config(config_default=config_default, section="CxReporting", prefix="cxreporting_")
    return Configuration(
        server_base_url=config.get("reporting_client_url"),
        token_url=f"{config.get('base_url')}/cxrestapi/auth/identity/connect/token",
        username=config.get("username"),
        password=config.get("password"),
        grant_type=config.get("grant_type"),
        scope=config.get("scope"),
        client_id=config.get("client_id"),
        client_secret=config.get("client_secret"),
        timeout=config.get("timeout"),
        verify=config.get("verify"),
        cert=config.get("cert"),
        proxies={
            "http": config.get("proxy"),
            "https": config.get("proxy"),
        }
    )
