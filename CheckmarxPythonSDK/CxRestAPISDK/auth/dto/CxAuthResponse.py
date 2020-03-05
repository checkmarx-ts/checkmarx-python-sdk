# encoding: utf-8


class CxAuthResponse(object):
    def __init__(self, access_token, expires_in, token_type):
        """
        the response object

        Args:
            access_token (str):
            expires_in (str):
            token_type (str):
        """
        self.access_token = access_token
        self.expires_in = expires_in
        self.token_type = token_type

    def __str__(self):
        return "CxAuthResponse(access_token={}, expires_in={}, token_type={})".format(
            self.access_token, self.expires_in, self.token_type
        )
