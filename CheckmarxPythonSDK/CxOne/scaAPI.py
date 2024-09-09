from ..CxScaApiSDK.api import (
    Sca
)
from .httpRequests import (
    get_request as get,
    post_request as post,
    put_request as put,
    delete_request as delete,
)


class ScaAPI(Sca):

    def __init__(self, get_request=get, post_request=post, put_request=put, delete_request=delete):
        Sca.__init__(self, get_request=get, post_request=post, put_request=put, delete_request=delete)
        self.get_request = get_request
        self.post_request = post_request
        self.put_request = put_request
        self.delete_request = delete_request

    def __str__(self):
        return """ScaAPI()"""
