from CheckmarxPythonSDK.configuration import Configuration
from CheckmarxPythonSDK.utilities.configUtility import get_config


def construct_configuration() -> Configuration:
    config_default = {
        "base_url": None,
        "username": None,
        "password": None,
        "grant_type": "password",
        "scope": "access_control_api sast_api",
        "client_id": "resource_owner_sast_client",
        "client_secret": "014DF517-39D1-4453-B7B3-9930C563627C",
        "scan_preset": "Checkmarx Default",
        "configuration": "Default Configuration",
        "team_full_name": "/CxServer",
        "max_try": 2,
        "report_folder": None,
        "timeout": 59,
        "verify": True,
        "cert": None,
        "proxy": None,
    }
    old_config = get_config(config_default=config_default, section="checkmarx", prefix="cxsast_")
    new_config = get_config(config_default=config_default, section="CxSAST", prefix="cxsast_")
    config = old_config
    if new_config.get("base_url"):
        config = new_config
    return Configuration(
                server_base_url=config.get("base_url"),
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
