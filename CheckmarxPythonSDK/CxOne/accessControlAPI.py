from CheckmarxPythonSDK.api_client import ApiClient
from CheckmarxPythonSDK.CxOne.config import construct_configuration
from typing import List, Optional
from CheckmarxPythonSDK.utilities.compat import OK, NO_CONTENT
from CheckmarxPythonSDK.CxOne.dto import (
    AstIdWithName,
    AstUser,
    Role,
)

import urllib.parse


class AccessControlAPI(object):
    def __init__(self, api_client: ApiClient = None):
        if api_client is None:
            configuration = construct_configuration()
            api_client = ApiClient(configuration=configuration)
        self.api_client = api_client
        self.base_url = f"{self.api_client.configuration.iam_base_url}/auth/realms"
        self.realm = self.api_client.configuration.tenant_name

    def get_groups(
        self,
        realm: str = None,
        group_name: str = None,
        limit: int = 10,
        first: int = 0,
        max_result_size: int = 10000,
        ids: List[str] = None,
    ) -> List[AstIdWithName]:
        """

        Args:
            realm (str):
            group_name (str): Used for searching the groups by name
                or by part of name.
            limit (int): Max amount of returned record. Applied if
                groupName param defined. Default value : 10
            first (int): Element to start from. Always applied.
                Default value : 0
            max_result_size (int): Max number of items. Always applied.
                Default value : 10000
            ids (List[str]): Ids of groups separated with comma. Has
                priority over the groupName parameter

        Returns:
            List[AstIdWithName]
        """
        if realm is None:
            realm = self.realm
        url = f"{self.base_url}/{realm}/pip/groups"
        params = {
            "groupName": group_name,
            "limit": limit,
            "first": first,
            "max": max_result_size,
            "ids": ids if ids is None else ",".join(ids),
        }
        response = self.api_client.call_api(
            method="GET",
            url=url,
            params=params,
        )
        item_list = response.json()
        return [AstIdWithName.from_dict(item) for item in item_list]

    def get_group_by_name(
        self,
        group_name: str,
        realm: str = None,
    ) -> Optional[AstIdWithName]:
        """

        Args:
            realm (str):
            group_name (str):

        Returns:
            Optional[AstIdWithName]
        """
        result = None
        if realm is None:
            realm = self.realm
        groups = self.get_groups(realm=realm, group_name=group_name)
        one_group = list(filter(lambda g: g.name == group_name, groups))
        if len(one_group) == 1:
            result = one_group[0]
        return result

    def get_users(
        self,
        realm: str = None,
        first: int = 0,
        max_result_size: int = 100,
        search: str = None,
        sort: str = None,
        order: str = None,
        without_groups: bool = False,
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
        if realm is None:
            realm = self.realm
        url = f"{self.base_url}/{realm}/users"
        params = {
            "first": first,
            "max": max_result_size,
            "search": search,
            "sort": sort,
            "order": order,
            "withoutGroups": without_groups,
        }
        response = self.api_client.call_api(
            method="GET",
            url=url,
            params=params,
        )
        item_list = response.json()
        return [AstUser.from_dict(item) for item in item_list]

    def get_users_by_groups(
        self,
        group_id: str,
        realm: str = None,
    ) -> List[AstUser]:
        """

        Args:
            realm (str):
            group_id (str):

        Returns:
            List[AstUser]
        """
        if realm is None:
            realm = self.realm
        url = f"{self.base_url}/{realm}/pip/users/group/{group_id}"
        response = self.api_client.call_api(
            method="GET",
            url=url,
        )
        item_list = response.json()
        return [AstUser.from_dict(item) for item in item_list]

    def get_users_count(
        self,
        realm: str = None,
    ) -> int:
        """
        Args:
            realm (str):

        Returns:
            int
        """
        if realm is None:
            realm = self.realm
        url = f"{self.base_url}/{realm}/users/count"
        response = self.api_client.call_api(
            method="GET",
            url=url,
        )
        item = response.json()
        return item.get("count")

    def get_logged_in_user_roles(
        self,
        realm: str = None,
    ) -> List[Role]:
        """

        Args:
            realm:

        Returns:
            List[Role]
        """
        if realm is None:
            realm = self.realm
        url = f"{self.base_url}/{realm}/user-roles"
        response = self.api_client.call_api(
            method="GET",
            url=url,
        )
        item_list = response.json()
        return [Role.from_dict(item) for item in item_list]

    # ---- Forget Device ----

    def post_forget_all_devices(self, realm: str = None) -> bool:
        """
        Forget all registered devices for the current user.

        Args:
            realm (str):

        Returns:
            bool
        """
        if realm is None:
            realm = self.realm
        url = f"{self.base_url}/{realm}/forget-all-devices"
        response = self.api_client.call_api(method="POST", url=url)
        return response.status_code == OK

    def get_forget_device(self, redirect_uri: str = None, realm: str = None) -> str:
        """
        Get redirect URL for forgetting a device.

        Args:
            redirect_uri (str): Optional redirect URI
            realm (str):

        Returns:
            Location header string
        """
        if realm is None:
            realm = self.realm
        url = f"{self.base_url}/{realm}/forget-device"
        params = {"redirect_uri": redirect_uri} if redirect_uri else None
        response = self.api_client.call_api(
            method="GET", url=url, params=params
        )
        return response.headers.get("Location", "")

    # ---- MFA / OTP ----

    def get_reset_otp(
        self,
        execution: str = None,
        client_id: str = None,
        tab_id: str = None,
        realm: str = None,
    ) -> str:
        """
        Get redirect URL for OTP reset.

        Args:
            execution (str):
            client_id (str):
            tab_id (str):
            realm (str):

        Returns:
            Location header string
        """
        if realm is None:
            realm = self.realm
        url = f"{self.base_url}/{realm}/reset-otp"
        params = {
            "execution": execution,
            "client_id": client_id,
            "tab_id": tab_id,
        }
        response = self.api_client.call_api(
            method="GET", url=url, params=params
        )
        return response.headers.get("Location", "")

    def post_reset_otp(self, id: str, realm: str = None) -> bool:
        """
        Reset OTP for a user.

        Args:
            id (str): User ID (uuid)
            realm (str):

        Returns:
            bool
        """
        if realm is None:
            realm = self.realm
        url = f"{self.base_url}/{realm}/reset-otp"
        response = self.api_client.call_api(
            method="POST", url=url, json={"id": id}
        )
        return response.status_code == OK

    # ---- PIP (Policy Information Point) ----

    def get_pip_users(
        self, term: str, limit: int = None, realm: str = None
    ) -> List[AstIdWithName]:
        """
        Search for users (PIP).

        Args:
            term (str): Search term (required)
            limit (int): Max results
            realm (str):

        Returns:
            List[AstIdWithName]
        """
        if realm is None:
            realm = self.realm
        url = f"{self.base_url}/{realm}/pip/users"
        params = {"term": term, "limit": limit}
        response = self.api_client.call_api(
            method="GET", url=url, params=params
        )
        return [AstIdWithName.from_dict(item) for item in response.json()]

    # ---- Group Managers ----

    def get_group_managers(self, realm: str = None) -> List[dict]:
        """
        Get all group managers.

        Args:
            realm (str):

        Returns:
            list of dict
        """
        if realm is None:
            realm = self.realm
        url = f"{self.base_url}/{realm}/group-manager"
        response = self.api_client.call_api(method="GET", url=url)
        return response.json()

    def get_group_manager_users(
        self, group_id: str, realm: str = None
    ) -> List[dict]:
        """
        Get users for a group manager.

        Args:
            group_id (str): Group ID (required)
            realm (str):

        Returns:
            list of dict
        """
        if realm is None:
            realm = self.realm
        url = f"{self.base_url}/{realm}/group-manager/users"
        params = {"groupId": group_id}
        response = self.api_client.call_api(
            method="GET", url=url, params=params
        )
        return response.json()

    def assign_group_manager(
        self, group_id: str, user_ids: List[str], realm: str = None
    ) -> bool:
        """
        Assign users as group managers.

        Args:
            group_id (str):
            user_ids (List[str]):
            realm (str):

        Returns:
            bool
        """
        if realm is None:
            realm = self.realm
        url = f"{self.base_url}/{realm}/group-manager/assign"
        body = {"groupId": group_id, "userIds": user_ids}
        response = self.api_client.call_api(
            method="POST", url=url, json=body
        )
        return response.status_code == NO_CONTENT

    def unassign_group_manager(
        self, group_id: str, user_ids: List[str], realm: str = None
    ) -> bool:
        """
        Unassign users from group managers.

        Args:
            group_id (str):
            user_ids (List[str]):
            realm (str):

        Returns:
            bool
        """
        if realm is None:
            realm = self.realm
        url = f"{self.base_url}/{realm}/group-manager/unassign"
        body = {"groupId": group_id, "userIds": user_ids}
        response = self.api_client.call_api(
            method="POST", url=url, json=body
        )
        return response.status_code == NO_CONTENT

    # ---- API Keys ----

    def get_api_keys(
        self, first: int = None, max: int = None, realm: str = None
    ) -> List[dict]:
        """
        Get all API keys.

        Args:
            first (int): Start index
            max (int): Max results
            realm (str):

        Returns:
            list of dict
        """
        if realm is None:
            realm = self.realm
        url = f"{self.base_url}/{realm}/api-keys"
        params = {"first": first, "max": max}
        response = self.api_client.call_api(
            method="GET", url=url, params=params
        )
        return response.json()

    def create_api_key(
        self,
        note: str = None,
        expiration_period: int = None,
        notification_emails: List[str] = None,
        realm: str = None,
    ) -> dict:
        """
        Create a new API key.

        Args:
            note (str): Note/description
            expiration_period (int): Days until expiration (30-365)
            notification_emails (List[str]): Notification email addresses
            realm (str):

        Returns:
            dict with client and key
        """
        if realm is None:
            realm = self.realm
        url = f"{self.base_url}/{realm}/api-keys"
        body = {
            "note": note,
            "expirationPeriod": expiration_period,
            "notificationEmails": notification_emails,
        }
        response = self.api_client.call_api(
            method="POST", url=url, json=body
        )
        return response.json()

    def get_api_keys_count(self, realm: str = None) -> int:
        """
        Get count of API keys.

        Args:
            realm (str):

        Returns:
            int
        """
        if realm is None:
            realm = self.realm
        url = f"{self.base_url}/{realm}/api-keys/count"
        response = self.api_client.call_api(method="GET", url=url)
        return response.json().get("count")

    def delete_api_key(self, session_id: str, realm: str = None) -> bool:
        """
        Delete an API key by session ID.

        Args:
            session_id (str):
            realm (str):

        Returns:
            bool
        """
        if realm is None:
            realm = self.realm
        url = f"{self.base_url}/{realm}/api-keys/{session_id}"
        response = self.api_client.call_api(method="DELETE", url=url)
        return response.status_code == OK

    # ---- Realm Owner ----

    def get_owner(self, realm: str = None) -> dict:
        """
        Get the realm owner.

        Args:
            realm (str):

        Returns:
            dict with id, username, firstName, lastName, email, activated
        """
        if realm is None:
            realm = self.realm
        url = f"{self.base_url}/{realm}/owner"
        response = self.api_client.call_api(method="GET", url=url)
        return response.json()

    def set_owner(
        self, username: str, realm: str = None
    ) -> bool:
        """
        Set the realm owner.

        Args:
            username (str):
            realm (str):

        Returns:
            bool
        """
        if realm is None:
            realm = self.realm
        url = f"{self.base_url}/{realm}/owner"
        body = {"username": username, "realm": realm or self.realm}
        response = self.api_client.call_api(
            method="POST", url=url, json=body
        )
        return response.status_code == OK

    # ---- Token Exchange ----

    def get_token_exchange(self, realm: str = None) -> dict:
        """
        Get a token exchange access token.

        Args:
            realm (str):

        Returns:
            dict with access_token, expires_in, refresh_token, etc.
        """
        if realm is None:
            realm = self.realm
        url = f"{self.base_url}/{realm}/token-exchange"
        response = self.api_client.call_api(method="GET", url=url)
        return response.json()

    def post_token_exchange_federation(
        self,
        username: str,
        password: str,
        otp: str = None,
        realm: str = None,
    ) -> bool:
        """
        Exchange a federation token.

        Args:
            username (str):
            password (str):
            otp (str): Optional OTP
            realm (str):

        Returns:
            bool
        """
        if realm is None:
            realm = self.realm
        url = f"{self.base_url}/{realm}/token-exchange/federation"
        data = {"username": username, "password": password}
        if otp:
            data["otp"] = otp
        response = self.api_client.call_api(
            method="POST",
            url=url,
            content=urllib.parse.urlencode(data),
            headers={"Content-Type": "application/x-www-form-urlencoded"},
        )
        return response.status_code == OK

    def post_service_token(
        self,
        target_realm: str,
        service_user: str = None,
        realm: str = None,
    ) -> dict:
        """
        Get a service token for a target realm.

        Args:
            target_realm (str): Target realm (required)
            service_user (str): Service user identifier
            realm (str):

        Returns:
            dict with access_token
        """
        if realm is None:
            realm = self.realm
        url = f"{self.base_url}/{realm}/service-token"
        body = {"targetRealm": target_realm, "serviceUser": service_user}
        response = self.api_client.call_api(
            method="POST", url=url, json=body
        )
        return response.json()

    # ---- Bulk Entities ----

    def post_bulk_entities_find(
        self, ids: List[str], type: str, realm: str = None
    ) -> List[dict]:
        """
        Find bulk entities by IDs.

        Args:
            ids (List[str]): Entity IDs (required)
            type (str): Entity type: user, group, or client (required)
            realm (str):

        Returns:
            list of dict with id and name
        """
        if realm is None:
            realm = self.realm
        url = f"{self.base_url}/{realm}/bulk-entities/find"
        body = urllib.parse.urlencode(
            {"ids": ",".join(ids), "type": type}
        )
        response = self.api_client.call_api(
            method="POST",
            url=url,
            content=body,
            headers={"Content-Type": "application/x-www-form-urlencoded"},
        )
        return response.json()


def get_groups(
    realm: str = None, group_name: str = None, limit: int = None, ids: str = None
) -> List[AstIdWithName]:
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
    without_groups: bool = False,
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


def post_forget_all_devices(realm: str = None) -> bool:
    return AccessControlAPI().post_forget_all_devices(realm=realm)


def get_forget_device(redirect_uri: str = None, realm: str = None) -> str:
    return AccessControlAPI().get_forget_device(
        redirect_uri=redirect_uri, realm=realm
    )


def get_reset_otp(
    execution: str = None,
    client_id: str = None,
    tab_id: str = None,
    realm: str = None,
) -> str:
    return AccessControlAPI().get_reset_otp(
        execution=execution, client_id=client_id, tab_id=tab_id, realm=realm
    )


def post_reset_otp(id: str, realm: str = None) -> bool:
    return AccessControlAPI().post_reset_otp(id=id, realm=realm)


def get_pip_users(
    term: str, limit: int = None, realm: str = None
) -> List[AstIdWithName]:
    return AccessControlAPI().get_pip_users(term=term, limit=limit, realm=realm)


def get_group_managers(realm: str = None) -> List[dict]:
    return AccessControlAPI().get_group_managers(realm=realm)


def get_group_manager_users(group_id: str, realm: str = None) -> List[dict]:
    return AccessControlAPI().get_group_manager_users(
        group_id=group_id, realm=realm
    )


def assign_group_manager(
    group_id: str, user_ids: List[str], realm: str = None
) -> bool:
    return AccessControlAPI().assign_group_manager(
        group_id=group_id, user_ids=user_ids, realm=realm
    )


def unassign_group_manager(
    group_id: str, user_ids: List[str], realm: str = None
) -> bool:
    return AccessControlAPI().unassign_group_manager(
        group_id=group_id, user_ids=user_ids, realm=realm
    )


def get_api_keys(
    first: int = None, max: int = None, realm: str = None
) -> List[dict]:
    return AccessControlAPI().get_api_keys(first=first, max=max, realm=realm)


def create_api_key(
    note: str = None,
    expiration_period: int = None,
    notification_emails: List[str] = None,
    realm: str = None,
) -> dict:
    return AccessControlAPI().create_api_key(
        note=note,
        expiration_period=expiration_period,
        notification_emails=notification_emails,
        realm=realm,
    )


def get_api_keys_count(realm: str = None) -> int:
    return AccessControlAPI().get_api_keys_count(realm=realm)


def delete_api_key(session_id: str, realm: str = None) -> bool:
    return AccessControlAPI().delete_api_key(session_id=session_id, realm=realm)


def get_owner(realm: str = None) -> dict:
    return AccessControlAPI().get_owner(realm=realm)


def set_owner(username: str, realm: str = None) -> bool:
    return AccessControlAPI().set_owner(username=username, realm=realm)


def get_token_exchange(realm: str = None) -> dict:
    return AccessControlAPI().get_token_exchange(realm=realm)


def post_token_exchange_federation(
    username: str, password: str, otp: str = None, realm: str = None
) -> bool:
    return AccessControlAPI().post_token_exchange_federation(
        username=username, password=password, otp=otp, realm=realm
    )


def post_service_token(
    target_realm: str, service_user: str = None, realm: str = None
) -> dict:
    return AccessControlAPI().post_service_token(
        target_realm=target_realm, service_user=service_user, realm=realm
    )


def post_bulk_entities_find(
    ids: List[str], type: str, realm: str = None
) -> List[dict]:
    return AccessControlAPI().post_bulk_entities_find(
        ids=ids, type=type, realm=realm
    )
