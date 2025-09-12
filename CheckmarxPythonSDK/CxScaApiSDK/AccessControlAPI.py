from CheckmarxPythonSDK.CxAccessControl.AccessControl import AccessControl
from CheckmarxPythonSDK.api_client import ApiClient
from CheckmarxPythonSDK.CxScaApiSDK.config import construct_configuration


class AccessControlAPI(AccessControl):
    def __init__(self, api_client: ApiClient = None, is_iam=True):
        if api_client is None:
            configuration = construct_configuration()
            api_client = ApiClient(configuration=configuration)
        self.is_iam = is_iam
        AccessControl.__init__(self, api_client=api_client, is_iam=is_iam)

    def __str__(self):
        return """AccessControlAPI()"""
