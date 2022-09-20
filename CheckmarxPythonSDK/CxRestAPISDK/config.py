from CheckmarxPythonSDK.utilities.configUtility import (
    get_config
)

config_default = {
    "base_url": "http://localhost:80",
    "username": "Admin",
    "password": "Password",
    "grant_type": "password",
    "scope": "sast_rest_api",
    "client_id": "resource_owner_client",
    "client_secret": "014DF517-39D1-4453-B7B3-9930C563627C",
    "scan_preset": "Checkmarx Default",
    "configuration": "Default Configuration",
    "team_full_name": "/CxServer",
    "max_try": 3,
    "report_folder": None,
    "timeout": 60,
    "verify": False,
    "cert": None,
}

config = get_config(config_default=config_default, section="checkmarx", prefix="cxsast_")

