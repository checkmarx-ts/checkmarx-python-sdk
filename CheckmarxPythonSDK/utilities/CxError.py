# encoding: utf-8
from CheckmarxPythonSDK.utilities.compat import (
    OK, BAD_REQUEST, NOT_FOUND, UNAUTHORIZED, FORBIDDEN, NO_CONTENT, CREATED, ACCEPTED
)


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


def check_response_status_code(response):
    """
    Just to be backward compatible with old code.
    Args:
        response:

    Returns:

    """
    status_code = response.status_code
    if status_code in [OK, CREATED, NO_CONTENT, ACCEPTED]:
        return
    elif status_code == BAD_REQUEST:
        raise BadRequestError(response.text)
    elif status_code == NOT_FOUND:
        raise NotFoundError()
    elif status_code == FORBIDDEN:
        raise CxError(
            response.text + " Please check the scope in your configuration file, please check if you have permission",
            status_code
        )
    else:
        raise CxError(response.text, status_code)
