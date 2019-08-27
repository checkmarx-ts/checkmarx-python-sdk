# encoding: utf-8


class CxCredential(object):
    """
    credential
    """
    def __init__(self, username, password):
        """

        Args:
            username (str):
            password (str):
        """
        self.username = username
        self.password = password

    def __str__(self):
        return "CxCredential(username={}, password={})".format(self.username, self.password)
