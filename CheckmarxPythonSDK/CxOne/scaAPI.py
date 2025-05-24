from ..CxScaApiSDK.api import (
    Sca
)
from .httpRequests import (
    get_request as get_re,
    post_request as post_re,
    put_request as put_re,
    delete_request as delete_re,
)

url_prefix = "/api/sca"


def get(relative_url, params=None, headers=None):
    return get_re(relative_url=url_prefix + relative_url, params=params, headers=headers)


def post(relative_url, data, params=None, headers=None, files=None):
    return post_re(relative_url=url_prefix + relative_url, data=data, files=files, params=params, headers=headers)


def put(relative_url, data, files=None, params=None, headers=None):
    return put_re(relative_url=url_prefix + relative_url, data=data, files=files, params=params, headers=headers)


def delete(relative_url, data=None, params=None, headers=None):
    return delete_re(relative_url=url_prefix + relative_url, data=data, params=params, headers=headers)


class ScaAPI(Sca):

    def __init__(self, get_request=get, post_request=post, put_request=put, delete_request=delete):
        Sca.__init__(self, get_request=get, post_request=post, put_request=put, delete_request=delete)
        self.get_request = get_request
        self.post_request = post_request
        self.put_request = put_request
        self.delete_request = delete_request
        self.gql_relative_url = "/graphql/graphql"

    def __str__(self):
        return """ScaAPI()"""
