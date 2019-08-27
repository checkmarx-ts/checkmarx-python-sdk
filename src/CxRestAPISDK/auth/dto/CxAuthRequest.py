# encoding: utf-8


class CxAuthRequest(object):
    """
    the request content to be sent in order to get token
    """

    def __init__(self, username, password, grant_type, scope, client_id, client_secret):
        """
        get attribute from configuration file by default
        :param username: str
        :param password: str
        :param grant_type: str
        :param scope: str
        :param client_id: str
        :param client_secret: str
        """
        self.username = username
        self.password = password
        self.grant_type = grant_type
        self.scope = scope
        self.client_id = client_id
        self.client_secret = client_secret

    def get_post_data(self):
        """
        get the data that will be posted in order to get token.
        :return:
        dict
            In Python package requests, the following statements about HTTP POST should be noted.
            Typically, you want to send some form-encoded data — much like an HTML form.
            To do this, simply pass a dictionary to the data argument.
            Your dictionary of data will automatically be form-encoded when the request is made.
        """
        return {
                "username": self.username,
                "password": self.password,
                "grant_type": self.grant_type,
                "scope": self.scope,
                "client_id": self.client_id,
                "client_secret": self.client_secret
            }

    def __str__(self):
        return """CxAuthRequest(username={}, password={}, grant_type={}, scope={}, 
                client_id={}, client_secret={})""".format(
            self.username, self.password, self.grant_type, self.scope, self.client_id, self.client_secret
        )
