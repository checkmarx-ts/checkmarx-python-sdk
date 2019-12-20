# encoding: utf-8
import http
import requests
import json

from ..auth import AuthenticationAPI
from ..config import CxConfig
from ..exceptions.CxError import BadRequestError, NotFoundError, UnknownHttpStatusError
from .dto import User, AuthenticationProvider


class AccessControlAPI(object):

    max_try = CxConfig.CxConfig.config.max_try
    base_url = CxConfig.CxConfig.config.url

    def __init__(self):
        self.retry = 0

    def get_all_assignable_users(self):

        assignable_users = None

        url = AccessControlAPI.base_url + "/auth/AssignableUsers"

        r = requests.get(
            url=url,
            headers=AuthenticationAPI.AuthenticationAPI.auth_headers
        )
        if r.status_code == http.HTTPStatus.OK:
            a_list = r.json()
            assignable_users = [
                User.User(
                    user_id=item.get("id"),
                    user_name=item.get("username"),
                    first_name=item.get("firstName"),
                    last_name=item.get("lastName"),
                    email=item.get("email")
                ) for item in a_list
            ]
        elif r.status_code == http.HTTPStatus.FORBIDDEN:
            pass
        elif r.status_code == http.HTTPStatus.BAD_REQUEST:
            raise BadRequestError(r.text)
        elif r.status_code == http.HTTPStatus.NOT_FOUND:
            raise NotFoundError()
        elif (r.status_code == http.HTTPStatus.UNAUTHORIZED) and (self.retry < self.max_try):
            AuthenticationAPI.AuthenticationAPI.reset_auth_headers()
            self.retry += 1
            self.get_all_assignable_users()
        else:
            raise UnknownHttpStatusError()

        self.retry = 0

        return assignable_users

    def get_all_authentication_providers(self):

        authentication_providers = None

        url = AccessControlAPI.base_url + "/auth/AuthenticationProviders"

        r = requests.get(
            url=url,
            headers=AuthenticationAPI.AuthenticationAPI.auth_headers
        )

        if r.status_code == http.HTTPStatus.OK:
            a_list = r.json()
            authentication_providers = [
                AuthenticationProvider.AuthenticationProvider(
                    id=item.get("id"),
                    name=item.get("name"),
                    provider_id=item.get("providerId"),
                    provider_type=item.get("providerType"),
                    is_external=item.get("isExternal"),
                    active=item.get("active")
                ) for item in a_list
            ]
        elif r.status_code == http.HTTPStatus.BAD_REQUEST:
            raise BadRequestError(r.text)
        elif r.status_code == http.HTTPStatus.NOT_FOUND:
            raise NotFoundError()
        elif (r.status_code == http.HTTPStatus.UNAUTHORIZED) and (self.retry < self.max_try):
            AuthenticationAPI.AuthenticationAPI.reset_auth_headers()
            self.retry += 1
            self.get_all_assignable_users()
        else:
            raise UnknownHttpStatusError()

        self.retry = 0

        return authentication_providers

    def submit_first_admin_user(self, username, password, first_name, last_name, email):
        """

        Args:
            username (str):
            password (str):
            first_name (str):
            last_name (str):
            email (str):

        Returns:

        """
        is_successful = False

        post_data = json.dumps({
            "username": username,
            "password": password,
            "firstName": first_name,
            "lastName": last_name,
            "email": email
        })

        url = AccessControlAPI.base_url + "/auth/Users/FirstAdmin"
        r = requests.post(
            url=url,
            data=post_data,
            headers=AuthenticationAPI.AuthenticationAPI.auth_headers
        )

        if r.status_code == http.HTTPStatus.CREATED:
            is_successful = True
        elif r.status_code == http.HTTPStatus.FORBIDDEN:
            pass
        elif r.status_code == http.HTTPStatus.BAD_REQUEST:
            raise BadRequestError(r.text)
        elif r.status_code == http.HTTPStatus.NOT_FOUND:
            raise NotFoundError()
        elif (r.status_code == http.HTTPStatus.UNAUTHORIZED) and (self.retry < self.max_try):
            AuthenticationAPI.AuthenticationAPI.reset_auth_headers()
            self.retry += 1
            self.submit_first_admin_user(username, password, first_name, last_name, email)
        else:
            raise UnknownHttpStatusError()

        self.retry = 0

        return is_successful

    def get_admin_user_exists_confirmation(self):

        first_admin_exists = False

        url = AccessControlAPI.base_url + "/auth/Users/FirstAdminExistence"
        r = requests.get(
            url=url,
            headers=AuthenticationAPI.AuthenticationAPI.auth_headers
        )

        if r.status_code == http.HTTPStatus.OK:
            d = r.json()
            if d.get("firstAdminExists"):
                first_admin_exists = True
        elif r.status_code == http.HTTPStatus.FORBIDDEN:
            pass
        elif r.status_code == http.HTTPStatus.BAD_REQUEST:
            raise BadRequestError(r.text)
        elif r.status_code == http.HTTPStatus.NOT_FOUND:
            raise NotFoundError()
        elif (r.status_code == http.HTTPStatus.UNAUTHORIZED) and (self.retry < self.max_try):
            AuthenticationAPI.AuthenticationAPI.reset_auth_headers()
            self.retry += 1
            self.get_admin_user_exists_confirmation()
        else:
            raise UnknownHttpStatusError()

        self.retry = 0

        return first_admin_exists
