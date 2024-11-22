from ..CxScaApiSDK.api import (
    Sca
)
from .httpRequests import (
    get_request as get_re,
    post_request as post_re,
    put_request as put_re,
    delete_request as delete_re,
    gql_request as gql_re
)

url_prefix = "/api/sca"


def get(relative_url):
    return get_re(relative_url=url_prefix + relative_url)


def post(relative_url, data, files=None):
    return post_re(relative_url=url_prefix + relative_url, data=data, files=files)


def put(relative_url, data, files=None):
    return put_re(relative_url=url_prefix + relative_url, data=data, files=files)


def delete(relative_url, data=None):
    return delete_re(relative_url=url_prefix + relative_url, data=data)


def gql(relative_url, data):
    return gql_re(relative_url=url_prefix + relative_url, data=data)


class ScaAPI(Sca):

    def __init__(self, get_request=get, post_request=post, put_request=put, delete_request=delete, gql_request=gql):
        Sca.__init__(self, get_request=get, post_request=post, put_request=put, delete_request=delete)
        self.get_request = get_request
        self.post_request = post_request
        self.put_request = put_request
        self.delete_request = delete_request
        self.gql_request = gql_request
        self.gql_relative_url = "/graphql/graphql"

    def __str__(self):
        return """ScaAPI()"""
