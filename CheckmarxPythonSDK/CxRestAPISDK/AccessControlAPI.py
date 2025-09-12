from CheckmarxPythonSDK.api_client import ApiClient
from CheckmarxPythonSDK.CxRestAPISDK.config import construct_configuration
from CheckmarxPythonSDK.CxAccessControl.AccessControl import AccessControl


class AccessControlAPI(AccessControl):
    def __init__(self, api_client: ApiClient = None):
        AccessControl.__init__(self, api_client=api_client)
        if api_client is None:
            configuration = construct_configuration()
            api_client = ApiClient(configuration=configuration)
        self.api_client = api_client

    def __str__(self):
        return """AccessControlAPI()"""
