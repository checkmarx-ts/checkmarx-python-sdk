# encoding: utf-8
import json
import requests
import time
import os
from CheckmarxPythonSDK.CxOne.httpRequests import get_request, post_request
from CheckmarxPythonSDK.CxOne import authHeaders
from CheckmarxPythonSDK.CxOne.config import config
from .dto import (
    Flag,
)

base_url = config.get("server")

def __construct_flag(flag):
    return Flag(
        name=flag.get("name"),
        status=flag.get("status"),
        payload=flag.get("payload")
    )

def get_all_feature_flags():
    """

    Returns:
        `list` of `Flag`
    """
    relative_url = f"/api/flags/"

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
    relative_url = f"/api/flags/{name}"

    response = get_request(relative_url=relative_url)

    flag = response.json()
    return __construct_flag(flag)
