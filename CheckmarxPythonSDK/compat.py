from requests.compat import is_py2

if is_py2:
    import httplib
    OK = httplib.OK
    BAD_REQUEST = httplib.BAD_REQUEST
    NOT_FOUND = httplib.NOT_FOUND
    UNAUTHORIZED = httplib.UNAUTHORIZED
    CREATED = httplib.CREATED
    FORBIDDEN = httplib.FORBIDDEN
    NO_CONTENT = httplib.NO_CONTENT
    ACCEPTED = httplib.ACCEPTED
    CONFLICT = httplib.CONFLICT
else:
    import http
    OK = http.HTTPStatus.OK
    BAD_REQUEST = http.HTTPStatus.BAD_REQUEST
    NOT_FOUND = http.HTTPStatus.NOT_FOUND
    UNAUTHORIZED = http.HTTPStatus.UNAUTHORIZED
    CREATED = http.HTTPStatus.CREATED
    FORBIDDEN = http.HTTPStatus.FORBIDDEN
    NO_CONTENT = http.HTTPStatus.NO_CONTENT
    ACCEPTED = http.HTTPStatus.ACCEPTED
    CONFLICT = http.HTTPStatus.CONFLICT
