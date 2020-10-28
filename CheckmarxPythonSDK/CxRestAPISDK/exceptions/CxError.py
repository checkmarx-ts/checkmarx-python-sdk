# encoding: utf-8


class CxError(Exception):
    """

    Args:
        msg (str): Human readable string describing the exception.
        code (:obj:`int`, optional): Error code.

    Attributes:
        msg (str): Human readable string describing the exception.
        code (int): Exception error code.
    """
    def __init__(self, msg, code):
        self.msg = msg
        self.code = code

    def __str__(self):
        return "CxError(msg={}, code={})".format(
            self.msg, self.code
        )


class BadRequestError(CxError):
    """
    http 400, bad request
    """

    def __init__(self, msg):
        super(BadRequestError, self).__init__(msg, 400)

    def __str__(self):
        return "BadRequestError(http_code=400, msg={})".format(self.msg)


class NotFoundError(CxError):
    """
    http 404, not found
    """

    def __init__(self, msg=None):
        super(NotFoundError, self).__init__(msg, 404)

    def __str__(self):
        return "NotFoundError(http_code=404, msg={}).".format(self.msg)
