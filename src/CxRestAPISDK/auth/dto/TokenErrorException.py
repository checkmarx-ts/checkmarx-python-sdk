# encoding: utf-8


class TokenErrorException(Exception):
    """
    Exception raised when get an access token error response

    Attributes:
        expression -- the expression when error occurred
        message -- explanation of the error
    """

    def __init__(self, expression, message):
        self.expression = expression
        self.message = message
