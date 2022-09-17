from CheckmarxPythonSDK.utilities.configUtility import (
    get_config
)

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
    "verify": False,
    "cert": None,
}

config = get_config(config_default=config_default, section="CxReporting", prefix="cxreporting_")
