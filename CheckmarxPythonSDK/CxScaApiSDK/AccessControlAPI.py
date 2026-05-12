from CheckmarxPythonSDK.CxAccessControl.AccessControl import AccessControl
from CheckmarxPythonSDK.api_client import ApiClient
from CheckmarxPythonSDK.CxScaApiSDK.config import construct_configuration


class AccessControlAPI(AccessControl):
    def __init__(self, api_client: ApiClient = None):
        if api_client is None:
            configuration = construct_configuration()
            api_client = ApiClient(configuration=configuration)
        ac_url = api_client.configuration.iam_base_url.rstrip("/")
        AccessControl.__init__(self, api_client=api_client, ac_url=ac_url)

    def __str__(self):
        return """AccessControlAPI()"""
