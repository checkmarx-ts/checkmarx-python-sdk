
from CheckmarxPythonSDK.configuration import Configuration
from CheckmarxPythonSDK.api_client import ApiClient
from CheckmarxPythonSDK.utilities.configUtility import get_config


if __name__ == '__main__':
    # configuration = Configuration(
    #     server_base_url="https://sng.ast.checkmarx.net/",
    #     iam_base_url="https://sng.iam.checkmarx.net/",
    #     token_url="https://sng.iam.checkmarx.net/auth/realms/happy/protocol/openid-connect/token",
    #     tenant_name="happy",
    #     grant_type="refresh_token",
    #     api_key="eyJhbGciOiJIUzUxMiIsInR5cCIgOiAiSldUIiwia2lkIiA6ICJmMmIwYTliNi1mZTZjLTQ4NmQtODliYS0wZjZhMTZlYzJhNTcifQ.eyJpYXQiOjE3NTUxNDkzMTksImp0aSI6IjU5Mjc0OGQ2LTgzNTYtNGJkNy1hMmMxLWQ5MGFjYTNhNWI5ZiIsImlzcyI6Imh0dHBzOi8vc25nLmlhbS5jaGVja21hcngubmV0L2F1dGgvcmVhbG1zL2hhcHB5IiwiYXVkIjoiaHR0cHM6Ly9zbmcuaWFtLmNoZWNrbWFyeC5uZXQvYXV0aC9yZWFsbXMvaGFwcHkiLCJzdWIiOiI1YTgxOTczZi1hMmZlLTRlN2MtOTgwOS0xMzQxN2UzMzIzYTYiLCJ0eXAiOiJPZmZsaW5lIiwiYXpwIjoiYXN0LWFwcCIsInNpZCI6ImVmOWY3NDBjLTkwNzItNDQwNi1iYzgyLWM5NDE0NGQxMDllYiIsInNjb3BlIjoiZW1haWwgYXN0LWFwaSBpYW0tYXBpIHJvbGVzIHByb2ZpbGUgb2ZmbGluZV9hY2Nlc3MifQ.ICEOQ_1Ocxw4WZSg3Rh3UhJzpJ7b06I_X9ZmYzi-FpFk4eHlU2exMG92jHKFE_2kbHdKhVgEDF2hvCDljEG5rQ"
    # )
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
        "verify": False,
        "cert": None,
        "proxy": None,
    }
    config = get_config(config_default=config_default, section="CxOne", prefix="cxone_")
    configuration = Configuration(
        server_base_url=config.get("server"),
        iam_base_url=config.get("access_control_url"),
        token_url=f"{config.get("access_control_url")}/auth/realms"
                  f"/{config.get("tenant_name")}/protocol/openid-connect/token",
        tenant_name=config.get("tenant_name"),
        grant_type=config.get("grant_type"),
        client_id=config.get("client_id"),
        client_secret=config.get("client_secret"),
        api_key=config.get("refresh_token"),
        timeout=config.get("timeout"),
        verify_ssl_cert=config.get("verify"),
        cert=config.get("cert"),
        proxies={
            "http": config.get("proxy"),
            "https": config.get("proxy"),
        }
    )
    api_client = ApiClient(configuration=configuration)
    response = api_client.get_request("/api/projects")
    pass
