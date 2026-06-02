from CheckmarxPythonSDK.api_client import ApiClient
from CheckmarxPythonSDK.CxOne.config import construct_configuration
from CheckmarxPythonSDK.utilities.compat import NO_CONTENT, CREATED


class CxLinkAPI(object):

    def __init__(self, api_client: ApiClient = None):
        if api_client is None:
            configuration = construct_configuration()
            api_client = ApiClient(configuration=configuration)
        self.api_client = api_client
        self.base_url = (
            f"{self.api_client.configuration.server_base_url}/api/v1/link"
        )

    def get_links(self, offset: int = 0, limit: int = 10) -> dict:
        """
        List all links.

        Args:
            offset (int): Starting point for pagination. Default: 0
            limit (int): Max records (max 1000). Default: 10

        Returns:
            dict with totalCount, items, _links
        """
        url = f"{self.base_url}/links"
        params = {"offset": offset, "limit": limit}
        response = self.api_client.call_api(
            method="GET", url=url, params=params
        )
        return response.json()

    def get_link(self, id: str) -> dict:
        """
        Retrieve a link by ID.

        Args:
            id (str): Link ID (uuid)

        Returns:
            dict with link details
        """
        url = f"{self.base_url}/links/{id}"
        response = self.api_client.call_api(method="GET", url=url)
        return response.json()

    def create_link(
        self,
        name: str = None,
        description: str = None,
        private_url: str = None,
    ) -> dict:
        """
        Create a new link.

        Args:
            name (str): Unique name for the link
            description (str): Optional description
            private_url (str): Private URL for the link

        Returns:
            dict with link, token, tunnelServerUrl
        """
        url = f"{self.base_url}/links"
        body = {}
        if name:
            body["name"] = name
        if description:
            body["description"] = description
        if private_url:
            body["privateUrl"] = private_url
        response = self.api_client.call_api(
            method="POST", url=url, json=body
        )
        if response.status_code == CREATED:
            return response.json()
        return response.json()

    def update_link(
        self, id: str, name: str = None, description: str = None
    ) -> bool:
        """
        Update a link. Only name and description can be changed.

        Args:
            id (str): Link ID (uuid)
            name (str): New unique name
            description (str): New description

        Returns:
            bool
        """
        url = f"{self.base_url}/links/{id}"
        body = {}
        if name:
            body["name"] = name
        if description:
            body["description"] = description
        response = self.api_client.call_api(
            method="PUT", url=url, json=body
        )
        return response.status_code == NO_CONTENT

    def delete_link(self, id: str) -> bool:
        """
        Delete a link.

        Args:
            id (str): Link ID (uuid)

        Returns:
            bool
        """
        url = f"{self.base_url}/links/{id}"
        response = self.api_client.call_api(method="DELETE", url=url)
        return response.status_code == NO_CONTENT

    def recreate_link(self, id: str) -> dict:
        """
        Recreate a link with new credentials.

        Args:
            id (str): Link ID (uuid)

        Returns:
            dict with new link details
        """
        url = f"{self.base_url}/links/{id}/recreate"
        response = self.api_client.call_api(method="PATCH", url=url)
        return response.json()


# ---- Module-level convenience functions ----

def get_links(offset: int = 0, limit: int = 10) -> dict:
    return CxLinkAPI().get_links(offset=offset, limit=limit)


def get_link(id: str) -> dict:
    return CxLinkAPI().get_link(id=id)


def create_link(
    name: str = None,
    description: str = None,
    private_url: str = None,
) -> dict:
    return CxLinkAPI().create_link(
        name=name, description=description, private_url=private_url
    )


def update_link(
    id: str, name: str = None, description: str = None
) -> bool:
    return CxLinkAPI().update_link(id=id, name=name, description=description)


def delete_link(id: str) -> bool:
    return CxLinkAPI().delete_link(id=id)


def recreate_link(id: str) -> dict:
    return CxLinkAPI().recreate_link(id=id)
