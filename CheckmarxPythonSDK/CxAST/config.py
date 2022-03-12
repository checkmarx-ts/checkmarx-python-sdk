from ..configUtility import (
    get_config
)

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
}

config = get_config(config_default=config_default, section="CxAST", prefix="cxast_")
