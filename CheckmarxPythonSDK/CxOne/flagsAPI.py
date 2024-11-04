# encoding: utf-8
import json
import requests
import time
import os
from CheckmarxPythonSDK.CxOne.httpRequests import get_request, post_request
from CheckmarxPythonSDK.CxOne.config import config
from .utilities import type_check, list_member_type_check
from .dto import (
    Flag,
)

base_url = config.get("server")

api_url = f"/api/flags/"


def __construct_flag(flag):
    return Flag(
        name=flag.get("name"),
        status=flag.get("status"),
        payload=flag.get("payload")
    )


def get_all_feature_flags(ids=None):
    """
    Args:
         ids (`list`)

    Returns:
        `list` of `Flag`
    """
    type_check(ids, (list, tuple))

    list_member_type_check(ids, str)

    relative_url = f"{api_url}"
    # We can't use get_url_param() because it assumes that this is not
    # the first query parameter.
    if ids:
        relative_url += f"?ids={','.join(ids)}"

    response = get_request(relative_url=relative_url)

    flags = response.json()
    return [__construct_flag(flag) for flag in flags]


def get_feature_flag(name):
    """

    Args:
        name (`str`)

    Returns:
        `Flag`
    """
    type_check(name, str)

    relative_url = f"{api_url}{name}"

    response = get_request(relative_url=relative_url)

    flag = response.json()
    return __construct_flag(flag)
