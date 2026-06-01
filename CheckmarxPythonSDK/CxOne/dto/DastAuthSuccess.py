from .StrEnum import StrEnum


class DastAuthSuccess(StrEnum):
    TRUE = "true"
    FALSE = "false"
    NO_AUTH = "no_auth"
    AUTH_NOT_SET = "auth_not_set"
