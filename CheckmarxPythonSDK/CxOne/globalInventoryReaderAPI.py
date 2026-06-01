from CheckmarxPythonSDK.api_client import ApiClient
from CheckmarxPythonSDK.CxOne.config import construct_configuration


class GlobalInventoryReaderAPI(object):

    def __init__(self, api_client: ApiClient = None):
        if api_client is None:
            configuration = construct_configuration()
            api_client = ApiClient(configuration=configuration)
        self.api_client = api_client
        self.base_url = (
            f"{self.api_client.configuration.server_base_url}"
            f"/api/apisec/global"
        )

    def get_api_changes(self, api_id: str = None, x_fields: str = None) -> dict:
        """
        Get changes for an API.

        Args:
            api_id (str): API ID
            x_fields (str): Optional fields mask

        Returns:
            dict with api_changes and last_update_date
        """
        url = f"{self.base_url}/api/api-changes/"
        params = {"api_id": api_id}
        headers = {}
        if x_fields:
            headers["X-Fields"] = x_fields
        response = self.api_client.call_api(
            method="GET", url=url, params=params, headers=headers
        )
        return response.json()

    def get_api_inventory(
        self,
        page: int = None,
        per_page: int = None,
        sorting: str = None,
        filtering: str = None,
        searching: str = None,
    ) -> dict:
        """
        Get all API inventory.

        Args:
            page (int): Page number
            per_page (int): Items per page
            sorting (str): Sort expression
            filtering (str): Filter expression
            searching (str): Full text search

        Returns:
            dict with entries and pagination info
        """
        url = f"{self.base_url}/api/inventory/"
        params = {
            "page": page,
            "per_page": per_page,
            "sorting": sorting,
            "filtering": filtering,
            "searching": searching,
        }
        response = self.api_client.call_api(
            method="GET", url=url, params=params
        )
        return response.json()

    def get_data_origin(self, api_id: str = None, x_fields: str = None) -> dict:
        """
        Get data origin for a given API.

        Args:
            api_id (str): API ID
            x_fields (str): Optional fields mask

        Returns:
            dict with entries array
        """
        url = f"{self.base_url}/api/inventory/data_origins"
        params = {"api_id": api_id}
        headers = {}
        if x_fields:
            headers["X-Fields"] = x_fields
        response = self.api_client.call_api(
            method="GET", url=url, params=params, headers=headers
        )
        return response.json()

    def get_api_inventory_group(
        self,
        group_column: str,
        page: int = None,
        per_page: int = None,
        sorting_order: str = None,
        filtering: str = None,
        searching: str = None,
        x_fields: str = None,
    ) -> dict:
        """
        Get API groups for global tables.

        Args:
            group_column (str): Column to group by (e.g. 'path')
            page (int): Page number
            per_page (int): Items per page
            sorting_order (str): Sort order (asc/desc)
            filtering (str): Filter expression
            searching (str): Full text search
            x_fields (str): Optional fields mask

        Returns:
            dict with groups and pagination info
        """
        url = f"{self.base_url}/api/inventory/group/{group_column}"
        params = {
            "page": page,
            "per_page": per_page,
            "sorting_order": sorting_order,
            "filtering": filtering,
            "searching": searching,
        }
        headers = {}
        if x_fields:
            headers["X-Fields"] = x_fields
        response = self.api_client.call_api(
            method="GET", url=url, params=params, headers=headers
        )
        return response.json()

    def get_inventory_metadata(self, x_fields: str = None) -> dict:
        """
        Get all API inventory metadata.

        Args:
            x_fields (str): Optional fields mask

        Returns:
            dict with column and options
        """
        url = f"{self.base_url}/api/inventory/metadata"
        headers = {}
        if x_fields:
            headers["X-Fields"] = x_fields
        response = self.api_client.call_api(
            method="GET", url=url, headers=headers
        )
        return response.json()

    def get_global_parameters(
        self, api_id: str = None, x_fields: str = None
    ) -> dict:
        """
        Get all parameters for the API.

        Args:
            api_id (str): API ID
            x_fields (str): Optional fields mask

        Returns:
            dict with request_parameters, response_parameters, piis, api_origins
        """
        url = f"{self.base_url}/api/parameter/"
        params = {"api_id": api_id}
        headers = {}
        if x_fields:
            headers["X-Fields"] = x_fields
        response = self.api_client.call_api(
            method="GET", url=url, params=params, headers=headers
        )
        return response.json()

    def get_api_risks(
        self,
        page: int = None,
        per_page: int = None,
        sorting: str = None,
        filtering: str = None,
        searching: str = None,
    ) -> dict:
        """
        Get all API risks.

        Args:
            page (int): Page number
            per_page (int): Items per page
            sorting (str): Sort expression
            filtering (str): Filter expression
            searching (str): Full text search

        Returns:
            dict
        """
        url = f"{self.base_url}/api/risk/"
        params = {
            "page": page,
            "per_page": per_page,
            "sorting": sorting,
            "filtering": filtering,
            "searching": searching,
        }
        response = self.api_client.call_api(
            method="GET", url=url, params=params
        )
        return response.json()

    def get_risk_groups(
        self,
        group_column: str,
        page: int = None,
        per_page: int = None,
        sorting_order: str = None,
        filtering: str = None,
        searching: str = None,
        x_fields: str = None,
    ) -> dict:
        """
        Get risk groups for global tables.

        Args:
            group_column (str): Column to group by (e.g. 'severity')
            page (int): Page number
            per_page (int): Items per page
            sorting_order (str): Sort order (asc/desc)
            filtering (str): Filter expression
            searching (str): Full text search
            x_fields (str): Optional fields mask

        Returns:
            dict with groups and pagination info
        """
        url = f"{self.base_url}/api/risk/group/{group_column}"
        params = {
            "page": page,
            "per_page": per_page,
            "sorting_order": sorting_order,
            "filtering": filtering,
            "searching": searching,
        }
        headers = {}
        if x_fields:
            headers["X-Fields"] = x_fields
        response = self.api_client.call_api(
            method="GET", url=url, params=params, headers=headers
        )
        return response.json()

    def get_risk_widget(self, api_id: str = None, x_fields: str = None) -> dict:
        """
        Get risk widget data.

        Args:
            api_id (str): API ID
            x_fields (str): Optional fields mask

        Returns:
            dict with entries, total_risks, last_update
        """
        url = f"{self.base_url}/api/risk/widget"
        params = {"api_id": api_id}
        headers = {}
        if x_fields:
            headers["X-Fields"] = x_fields
        response = self.api_client.call_api(
            method="GET", url=url, params=params, headers=headers
        )
        return response.json()

    def get_risk_details(self, risk_id: str, x_fields: str = None) -> dict:
        """
        Get risk details and total PII found for the related API.

        Args:
            risk_id (str): Risk UUID
            x_fields (str): Optional fields mask

        Returns:
            dict with vulnerability, status, source_node, etc.
        """
        url = f"{self.base_url}/api/risk/{risk_id}"
        headers = {}
        if x_fields:
            headers["X-Fields"] = x_fields
        response = self.api_client.call_api(
            method="GET", url=url, headers=headers
        )
        return response.json()


# ---- Module-level convenience functions ----

def get_api_changes(api_id: str = None, x_fields: str = None) -> dict:
    return GlobalInventoryReaderAPI().get_api_changes(
        api_id=api_id, x_fields=x_fields
    )


def get_api_inventory(
    page: int = None,
    per_page: int = None,
    sorting: str = None,
    filtering: str = None,
    searching: str = None,
) -> dict:
    return GlobalInventoryReaderAPI().get_api_inventory(
        page=page, per_page=per_page, sorting=sorting,
        filtering=filtering, searching=searching,
    )


def get_data_origin(api_id: str = None, x_fields: str = None) -> dict:
    return GlobalInventoryReaderAPI().get_data_origin(
        api_id=api_id, x_fields=x_fields
    )


def get_api_inventory_group(
    group_column: str,
    page: int = None,
    per_page: int = None,
    sorting_order: str = None,
    filtering: str = None,
    searching: str = None,
    x_fields: str = None,
) -> dict:
    return GlobalInventoryReaderAPI().get_api_inventory_group(
        group_column=group_column, page=page, per_page=per_page,
        sorting_order=sorting_order, filtering=filtering,
        searching=searching, x_fields=x_fields,
    )


def get_inventory_metadata(x_fields: str = None) -> dict:
    return GlobalInventoryReaderAPI().get_inventory_metadata(x_fields=x_fields)


def get_global_parameters(
    api_id: str = None, x_fields: str = None
) -> dict:
    return GlobalInventoryReaderAPI().get_global_parameters(
        api_id=api_id, x_fields=x_fields
    )


def get_api_risks(
    page: int = None,
    per_page: int = None,
    sorting: str = None,
    filtering: str = None,
    searching: str = None,
) -> dict:
    return GlobalInventoryReaderAPI().get_api_risks(
        page=page, per_page=per_page, sorting=sorting,
        filtering=filtering, searching=searching,
    )


def get_risk_groups(
    group_column: str,
    page: int = None,
    per_page: int = None,
    sorting_order: str = None,
    filtering: str = None,
    searching: str = None,
    x_fields: str = None,
) -> dict:
    return GlobalInventoryReaderAPI().get_risk_groups(
        group_column=group_column, page=page, per_page=per_page,
        sorting_order=sorting_order, filtering=filtering,
        searching=searching, x_fields=x_fields,
    )


def get_risk_widget(api_id: str = None, x_fields: str = None) -> dict:
    return GlobalInventoryReaderAPI().get_risk_widget(
        api_id=api_id, x_fields=x_fields
    )


def get_risk_details(risk_id: str, x_fields: str = None) -> dict:
    return GlobalInventoryReaderAPI().get_risk_details(
        risk_id=risk_id, x_fields=x_fields
    )
