from CheckmarxPythonSDK.api_client import ApiClient
from CheckmarxPythonSDK.CxOne.config import construct_configuration
from typing import List
from CheckmarxPythonSDK.CxOne.dto import (
    AstIdWithName, construct_ast_id_with_name,
    AstUser, construct_ast_user,
    Role, construct_role,
)

api_url = f"/auth/realms"


class AccessControlAPI(object):
    def __init__(self, api_client: ApiClient = None):
        if api_client is None:
            configuration = construct_configuration()
            api_client = ApiClient(configuration=configuration)
        self.api_client = api_client

    def get_groups(
            self,
            realm: str,
            group_name: str = None,
            limit: int = 10,
            first: int = 0,
            max_result_size: int = 10000,
            ids: List[str] = None
    ) -> List[AstIdWithName]:
        """

        Args:
            realm (str):
            group_name (str): Used for searching the groups by name or by part of name.
            limit (int): Max amount of returned record. Applied if groupName param defined. Default value : 10
            first (int): Element to start from. Always applied. Default value : 0
            max_result_size (int): Max number of items. Always applied. Default value : 10000
            ids (List[str]): Ids of groups separated with comma. Has priority over the groupName parameter

        Returns:
            List[AstIdWithName]
        """
        relative_url = api_url + f"/{realm}/pip/groups"
        params = {
            "groupName": group_name,
            "limit": limit,
            "first": first,
            "max": max_result_size,
            "ids": ids if ids is None else ",".join(ids),
        }
        response = self.api_client.get_request(relative_url=relative_url, params=params, is_iam=True)
        item_list = response.json()
        return [construct_ast_id_with_name(item) for item in item_list]

    def get_group_by_name(self, realm: str, group_name: str) -> AstIdWithName:
        """

        Args:
            realm (str):
            group_name (str):

        Returns:
            Group
        """
        result = None
        groups = self.get_groups(realm=realm, group_name=group_name)
        one_group = list(filter(lambda g: g.name == group_name, groups))
        if len(one_group) == 1:
            result = one_group[0]
        return result

    def get_users(
            self,
            realm: str,
            first: int = 0,
            max_result_size: int = 100,
            search: str = None,
            sort: str = None,
            order: str = None,
            without_groups: bool = False
    ) -> List[AstUser]:
        """

        Args:
            realm (str):
            first (int):
            max_result_size (int): Max amount of returned records
            search (str):
            sort (str):
            order (str):
            without_groups (bool): default value: false

        Returns:
            List[AstUser]
        """
        relative_url = api_url + f"/{realm}/users"
        params = {
            "first": first,
            "max": max_result_size,
            "search": search,
            "sort": sort,
            "order": order,
            "withoutGroups": without_groups,
        }
        response = self.api_client.get_request(relative_url=relative_url, params=params, is_iam=True)
        item_list = response.json()
        return [construct_ast_user(item) for item in item_list]

    def get_users_by_groups(self, realm: str, group_id: str) -> List[AstUser]:
        """

        Args:
            realm (str):
            group_id (str):

        Returns:
            List[AstUser]
        """
        relative_url = api_url + f"/{realm}/pip/users/group/{group_id}"
        response = self.api_client.get_request(relative_url=relative_url, is_iam=True)
        item_list = response.json()
        return [construct_ast_user(item) for item in item_list]

    def get_users_count(self, realm: str) -> int:
        """
        Args:
            realm (str):

        Returns:
            int
        """
        relative_url = f"{api_url}/{realm}/users/count"
        response = self.api_client.get_request(relative_url=relative_url, is_iam=True)
        item = response.json()
        return item.get("count")

    def get_logged_in_user_roles(self, realm: str) -> List[Role]:
        """

        Args:
            realm:

        Returns:
            List[Role]
        """
        relative_url = f"{api_url}/{realm}/user-roles"
        response = self.api_client.get_request(relative_url=relative_url, is_iam=True)
        item_list = response.json()
        return [construct_role(item) for item in item_list]


def get_groups(realm: str, group_name: str = None, limit: int = None, ids: str = None) -> List[AstIdWithName]:
    return AccessControlAPI().get_groups(
        realm=realm, group_name=group_name, limit=limit, ids=ids
    )


def get_group_by_name(realm: str, group_name: str) -> AstIdWithName:
    return AccessControlAPI().get_group_by_name(realm=realm, group_name=group_name)


def get_users(
        realm: str,
        first: int = 0,
        max_result_size: int = 100,
        search: str = None,
        sort: str = None,
        order: str = None,
        without_groups: bool = False
) -> List[AstUser]:
    return AccessControlAPI().get_users(
        realm=realm,
        first=first,
        max_result_size=max_result_size,
        search=search,
        sort=sort,
        order=order,
        without_groups=without_groups,
    )


def get_users_by_groups(realm: str, group_id: str) -> List[AstUser]:
    return AccessControlAPI().get_users_by_groups(realm=realm, group_id=group_id)


def get_users_count(realm: str) -> int:
    return AccessControlAPI().get_users_count(realm=realm)


def get_logged_in_user_roles(realm: str) -> List[Role]:
    return AccessControlAPI().get_logged_in_user_roles(realm=realm)
