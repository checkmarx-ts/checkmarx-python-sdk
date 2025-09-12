from CheckmarxPythonSDK.CxScaApiSDK.api import Sca
from CheckmarxPythonSDK.api_client import ApiClient
from CheckmarxPythonSDK.CxOne.config import construct_configuration


class ScaAPI(Sca):

    def __init__(self, api_client: ApiClient = None):
        if api_client is None:
            configuration = construct_configuration()
            api_client = ApiClient(configuration=configuration, url_prefix="/api/sca")
        Sca.__init__(self, api_client=api_client)

    def __str__(self):
        return """ScaAPI()"""
