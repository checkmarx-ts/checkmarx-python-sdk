from CheckmarxPythonSDK.api_client import ApiClient
from CheckmarxPythonSDK.CxOne.config import construct_configuration
import json
from typing import List, Union
from ...utilities.compat import CREATED, OK, NO_CONTENT
from ..utilities import get_url_param, type_check
from .url import api_url
from .dto import UserRepresentation, User, construct_user


class UsersAPI(object):

    def __init__(self, api_client: ApiClient = None):
        if api_client is None:
            configuration = construct_configuration()
            api_client = ApiClient(configuration=configuration)
        self.api_client = api_client

    def get_users(
            self,
            realm: str,
            brief_representation: bool = False,
            email: str = None,
            email_verified: bool = None,
            enabled: bool = None,
            exact: bool = None,
            first: int = None,
            first_name: str = None,
            idp_alias: str = None,
            idp_user_id: str = None,
            last_name: str = None,
            max_result_size: int = 1024,
            search: str = None,
            username: str = None
    ) -> List[User]:
        """
        Returns a stream of users, filtered according to query parameters

        Args:
            realm (str): realm name (not id!)
            brief_representation (bool): Boolean which defines whether brief representations are returned (default: false)
            email (str): A String contained in email, or the complete email, if param "exact" is true
            email_verified (bool): whether the email has been verified
            enabled (bool): representing if user is enabled or not
            exact (bool): which defines whether the params "last", "first", "email" and "username" must match exactly
            first (int): Pagination offset
            first_name (str): A String contained in firstName, or the complete firstName, if param "exact" is true
            idp_alias (str): The alias of an Identity Provider linked to the user
            idp_user_id (str): The userId at an Identity Provider linked to the user
            last_name (str): A String contained in lastName, or the complete lastName, if param "exact" is true
            max_result_size (int): Maximum results size (defaults to 100)
            search (str): A String contained in username, first or last name, or email
            username (str): A String contained in username, or the complete username, if param "exact" is true

        Returns:
            list of User
        """
        type_check(realm, str)
        type_check(brief_representation, bool)
        type_check(email, str)
        type_check(email_verified, bool)
        type_check(enabled, bool)
        type_check(exact, bool)
        type_check(first, int)
        type_check(first_name, str)
        type_check(idp_alias, str)
        type_check(idp_user_id, str)
        type_check(last_name, str)
        type_check(max_result_size, int)
        type_check(search, str)
        type_check(username, str)

        relative_url = api_url + "/{realm}/users?".format(realm=realm)
        params = {
            "briefRepresentation": brief_representation, "email": email, "emailVerified": email_verified,
            "enabled": enabled, "exact": exact, "first": first, "firstName": first_name,
            "idpAlias": idp_alias, "idpUserId": idp_user_id, "lastName": last_name, "max": max_result_size,
            "search": search, "username": username,
        }

        response = self.api_client.get_request(relative_url=relative_url, params=params, is_iam=True)
        users = response.json()
        return [construct_user(user) for user in users]

    @staticmethod
    def filter_user_id_by_name(users: List[User], username: str) -> Union[str, None]:
        """

        Args:
            users (list of User):
            username (str):

        Returns:
            str or None
        """
        users_by_name = list(filter(lambda r: r.username == username, users))
        if not users_by_name:
            return None
        user = users_by_name[0]
        user_id = user.id
        return user_id

    def get_user_id_by_name(self, realm: str, username: str) -> str:
        """

        Args:
            realm (str):
            username (str):

        Returns:
            str
        """
        users = self.get_users(realm=realm)
        user_id = self.filter_user_id_by_name(users, username)
        return user_id

    def get_user_id_list_by_username_list(self, realm: str, username_list: List[str]) -> List[str]:
        """

        Args:
            realm (str):
            username_list (list of str):

        Returns:
            list of str
        """
        users = self.get_users(realm=realm)
        return [self.filter_user_id_by_name(users, username) for username in username_list]

    @staticmethod
    def filter_user_id_by_email(users, email):
        """

        Args:
            users:
            email:

        Returns:

        """
        users_by_email = list(filter(lambda r: r.email == email, users))
        if not users_by_email:
            return None
        user = users_by_email[0]
        user_id = user.id
        return user_id

    def get_user_id_by_email(self, realm: str, email: str) -> str:
        """

        Args:
            realm (str):
            email (str):

        Returns:
            str
        """
        users = self.get_users(realm=realm)
        user_id = self.filter_user_id_by_email(users, email)
        return user_id

    def get_user_id_list_by_email_list(self, realm: str, email_list: str):
        users = self.get_users(realm=realm)
        return [self.filter_user_id_by_email(users, email) for email in email_list]

    def create_a_new_user(
            self,
            realm: str,
            username: str,
            email: str,
            first_name: str,
            last_name: str,
            enabled: bool = True,
            attributes: dict = None,
            groups: List[str] = None,
            email_verified: bool = False,
            required_actions: List[str] = None
    ) -> bool:
        """
        Username must be unique.
        Args:
            realm (str): realm name (not id!)
            username (str):
            email (str):
            first_name (str):
            last_name (str):
            enabled (bool): user enabled
            attributes (dict): example: {"other":["ccc for test"]}
            groups (list of str):
            email_verified (bool):
            required_actions (list of str): example: ["UPDATE_PASSWORD"]

        Returns:
            bool
        """
        result = False
        relative_url = api_url + "/{realm}/users?".format(realm=realm)
        type_check(username, str)
        type_check(email, str)
        type_check(first_name, str)
        type_check(last_name, str)
        type_check(enabled, bool)
        type_check(attributes, dict)
        type_check(groups, list)
        type_check(email_verified, bool)
        type_check(required_actions, list)
        data = {
            "enabled": enabled,
            "attributes": attributes or {},
            "groups": groups or [],
            "emailVerified": email_verified,
            "username": username,
            "email": email,
            "firstName": first_name,
            "lastName": last_name,
        }
        if required_actions:
            data.update({"requiredActions": required_actions or []})
        data = json.dumps(data)
        response = self.api_client.post_request(relative_url=relative_url, data=data, is_iam=True)
        return response.status_code == CREATED

    def get_number_of_users_by_given_criteria(
            self,
            realm: str,
            email: str = None,
            email_verified: str = None,
            enabled: bool = None,
            first_name: str = None,
            last_name: str = None,
            q: str = None,
            search: str = None,
            username: str = None
    ) -> dict:
        """
            Returns the number of users that match the given criteria.
        Args:
            realm (str):  realm name (not id!)
            email (str): email filter
            email_verified (str):
            enabled (bool): Boolean representing if user is enabled or not
            first_name (str): first name filter
            last_name (str):
            q (str):
            search (str): arbitrary search string for all the fields below. Default search behavior is prefix-based
                    (e.g., foo or foo*). Use foo for infix search and "foo" for exact search.
            username (str): username filter

        Returns:
            int
        """
        relative_url = api_url + f"/{realm}/users/count"
        relative_url += get_url_param("email", email)
        relative_url += get_url_param("emailVerified", email_verified)
        relative_url += get_url_param("enabled", enabled)
        relative_url += get_url_param("firstName", first_name)
        relative_url += get_url_param("lastName", last_name)
        relative_url += get_url_param("q", q)
        relative_url += get_url_param("search", search)
        relative_url += get_url_param("username", username)
        params = {
            "email": email, "emailVerified": email_verified, "enabled": enabled, "firstName": first_name,
            "lastName": last_name, "q": q, "search": search, "username": username
        }
        response = self.api_client.get_request(relative_url=relative_url, params=params, is_iam=True)
        result = response.json()
        return result

    def delete_user(self, realm: str, user_id: str) -> bool:
        """

        Args:
            realm (str):  realm name (not id!)
            user_id (str):

        Returns:

        """
        result = False
        relative_url = api_url + f"/{realm}/users/{user_id}"
        type_check(realm, str)
        type_check(user_id, str)
        response = self.api_client.delete_request(relative_url=relative_url, is_iam=True)
        return response.status_code == NO_CONTENT

    def get_users_profile(self, realm: str) -> dict:
        """

        Args:
            realm (str):

        Returns:

        """
        relative_url = api_url + f"/{realm}/users/profile"
        response = self.api_client.get_request(relative_url=relative_url, is_iam=True)
        return response.json()

    def get_users_profile_metadata(self, realm: str) -> dict:
        """

        Args:
            realm:

        Returns:

        """
        relative_url = api_url + f"/{realm}/users/profile/metadata"
        response = self.api_client.get_request(relative_url=relative_url, is_iam=True)
        return response.json()

    def get_user_by_id(self, realm: str, user_id: str) -> dict:
        """

        Args:
            realm (str):
            user_id (str):

        Returns:

        """
        type_check(realm, str)
        type_check(user_id, str)
        relative_url = api_url + f"/{realm}/users/{user_id}"
        response = self.api_client.get_request(relative_url=relative_url, is_iam=True)
        return response.json()

    def update_user_by_id(
            self,
            realm: str,
            user_id: str,
            username: str,
            first_name: str,
            last_name: str,
            email: str,
            email_verified: bool = True,
            user_enabled: bool = True,
            totp: bool = False,
            required_actions: List[str] = None,
            manage_group_members_ship_access: bool = True,
            view_access: bool = True,
            map_roles_access: bool = True,
            impersonate_access: bool = True,
            manage_access: bool = True,
            attributes: dict = None
    ) -> bool:
        relative_url = api_url + f"/{realm}/users/{user_id}"
        data = {
            "username": username, "firstName": first_name, "lastName": last_name, "email": email,
            "emailVerified": email_verified, "enabled": user_enabled, "totp": totp,
            "disableableCredentialTypes": [], "requiredActions": required_actions or [], "notBefore": 0,
            "access": {
                "manageGroupMembership": manage_group_members_ship_access, "view": view_access,
                "mapRoles": map_roles_access, "impersonate": impersonate_access,
                "manage": manage_access
            },
        }
        if attributes:
            data.update({"attributes": attributes})
        data = json.dumps(data)
        response = self.api_client.put_request(relative_url=relative_url, data=data, is_iam=True)
        return response.status_code == NO_CONTENT


def get_users(
            realm: str,
            brief_representation: bool = False,
            email: str = None,
            email_verified: bool = None,
            enabled: bool = None,
            exact: bool = None,
            first: int = None,
            first_name: str = None,
            idp_alias: str = None,
            idp_user_id: str = None,
            last_name: str = None,
            max_result_size: int = 1024,
            search: str = None,
            username: str = None
    ) -> List[User]:
    return UsersAPI().get_users(
        realm=realm, brief_representation=brief_representation, email=email, email_verified=email_verified,
        enabled=enabled, exact=exact, first=first, first_name=first_name, idp_alias=idp_alias,
        idp_user_id=idp_user_id, last_name=last_name, max_result_size=max_result_size,
        search=search, username=username,
    )


def filter_user_id_by_name(users: List[User], username: str) -> Union[str, None]:
    return UsersAPI().filter_user_id_by_name(users=users, username=username)


def get_user_id_by_name(realm: str, username: str) -> str:
    return UsersAPI().get_user_id_by_name(realm=realm, username=username)


def get_user_id_list_by_username_list(realm: str, username_list: List[str]) -> List[str]:
    return UsersAPI().get_user_id_list_by_username_list(realm=realm, username_list=username_list)


def filter_user_id_by_email(users, email):
    return UsersAPI().filter_user_id_by_email(users=users, email=email)


def get_user_id_by_email(realm: str, email: str) -> str:
    return UsersAPI().get_user_id_by_email(realm=realm, email=email)


def get_user_id_list_by_email_list(realm: str, email_list: str):
    return UsersAPI().get_user_id_list_by_email_list(realm=realm, email_list=email_list)


def create_a_new_user(
            realm: str,
            username: str,
            email: str,
            first_name: str,
            last_name: str,
            enabled: bool = True,
            attributes: dict = None,
            groups: List[str] = None,
            email_verified: bool = False,
            required_actions: List[str] = None
    ) -> bool:
    return UsersAPI().create_a_new_user(
       realm=realm, username=username, email=email, first_name=first_name, last_name=last_name, enabled=enabled,
        attributes=attributes, groups=groups, email_verified=email_verified, required_actions=required_actions,
    )


def get_number_of_users_by_given_criteria(
            realm: str,
            email: str = None,
            email_verified: str = None,
            enabled: bool = None,
            first_name: str = None,
            last_name: str = None,
            q: str = None,
            search: str = None,
            username: str = None
    ) -> dict:
    return UsersAPI().get_number_of_users_by_given_criteria(
       realm=realm, email=email, email_verified=email_verified, enabled=enabled, first_name=first_name,
        last_name=last_name, q=q, search=search, username=username,
    )


def delete_user(realm: str, user_id: str) -> bool:
    return UsersAPI().delete_user(realm=realm, user_id=user_id)


def get_users_profile(realm: str) -> dict:
    return UsersAPI().get_users_profile(realm=realm)


def get_users_profile_metadata(realm: str) -> dict:
    return UsersAPI().get_users_profile_metadata(realm=realm)


def get_user_by_id(realm: str, user_id: str) -> dict:
    return UsersAPI().get_user_by_id(realm=realm, user_id=user_id)


def update_user_by_id(
            realm: str,
            user_id: str,
            username: str,
            first_name: str,
            last_name: str,
            email: str,
            email_verified: bool = True,
            user_enabled: bool = True,
            totp: bool = False,
            required_actions: List[str] = None,
            manage_group_members_ship_access: bool = True,
            view_access: bool = True,
            map_roles_access: bool = True,
            impersonate_access: bool = True,
            manage_access: bool = True,
            attributes: dict = None
    ) -> bool:
    return UsersAPI().update_user_by_id(
        realm=realm, user_id=user_id, username=username, first_name=first_name, last_name=last_name, email=email,
        email_verified=email_verified, user_enabled=user_enabled, totp=totp, required_actions=required_actions,
        manage_group_members_ship_access=manage_group_members_ship_access, view_access=view_access,
        map_roles_access=map_roles_access, impersonate_access=impersonate_access, manage_access=manage_access,
        attributes=attributes
    )


