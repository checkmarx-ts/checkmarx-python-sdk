# encoding: utf-8
import json
import requests
import time
import os
from CheckmarxPythonSDK.CxOne.httpRequests import get_request, post_request
from CheckmarxPythonSDK.CxOne.config import config
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


def get_all_feature_flags():
    """

    Returns:
        `list` of `Flag`
    """
    if not config['tenant_id']:
        _set_tenant_id()

    relative_url = f"{api_url}?filter={config['tenant_id']}"

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
    if not config['tenant_id']:
        _set_tenant_id()

    relative_url = f"{api_url}{name}?filter={config['tenant_id']}"

    response = get_request(relative_url=relative_url)

    flag = response.json()
    return __construct_flag(flag)


def _set_tenant_id():

    resp = get_request(f"/auth/admin/realms/{config['tenant_name']}",
                       is_iam=True)
    config['tenant_id'] = resp.json()['id']
