from CheckmarxPythonSDK.utilities.configUtility import (
    get_config
)

config_default = {
    "access_control_url": "https://platform.checkmarx.net",
    "server": "https://api-sca.checkmarx.net",
    "account": None,
    "username": None,
    "password": None,
    "scope": "sca_api access_control_api",
    "timeout": 60,
    "verify": False,
    "cert": None,
}

config = get_config(config_default=config_default, section="CxSCA", prefix="cxsca_")
