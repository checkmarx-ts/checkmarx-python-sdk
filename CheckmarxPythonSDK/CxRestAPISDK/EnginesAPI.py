import json
from typing import List
from CheckmarxPythonSDK.api_client import ApiClient
from CheckmarxPythonSDK.CxRestAPISDK.config import construct_configuration, get_headers
from CheckmarxPythonSDK.utilities.compat import OK, NO_CONTENT, CREATED
from .sast.engines.dto import (
    CxEngineServer,
    CxEngineConfiguration,
    CxEngineDedication,
)


class EnginesAPI(object):
    """
    engines API
    """

    def __init__(self, api_client: ApiClient = None):
        if api_client is None:
            configuration = construct_configuration()
            api_client = ApiClient(configuration=configuration)
        self.api_client = api_client
        self.base_url = api_client.configuration.server_base_url.rstrip("/")

    def get_all_engine_server_details(
        self, api_version: str = "5.0"
    ) -> List[CxEngineServer]:
        """
        GET /sast/engineServers Gets details of all Engine Servers
        Args:
            api_version (str, optional):

        Returns:
            :obj:`CxEngineServer`

        Raises:
            BadRequestError
            NotFoundError
            CxError
        """
        result = None
        url = f"{self.base_url}/cxrestapi/sast/engineServers"
        response = self.api_client.call_api(
            "GET", url, headers=get_headers(api_version)
        )
        if response.status_code == OK:
            result = [CxEngineServer.from_dict(item) for item in response.json()]
        return result

    def get_engine_id_by_name(self, engine_name: str) -> int:
        """

        Args:
            engine_name (str):

        Returns:
            int: engine id
        """
        all_engine_servers = self.get_all_engine_server_details()
        a_dict = {item.name: item.id for item in all_engine_servers}
        return a_dict.get(engine_name)

    def register_engine(
        self,
        name: str,
        uri: str,
        min_loc: int,
        max_loc: int,
        is_blocked: bool,
        max_scans: int,
        dedications: List[CxEngineDedication] = None,
        api_version: str = "5.0",
    ) -> CxEngineServer:
        """
        POST  /sast/engineServers  Registers an Engine Server
        Args:
            name (str): Name of the engine server
            uri (str): Specifies the url of the engine server
            min_loc (int): Specifies the minimum number of lines of code to scan
            max_loc (int): Specifies the maximum number of lines of code to scan
            is_blocked (boolean): Specifies whether or not the engine will be able to receive scan requests
            max_scans (int):
            dedications (`list` of :obj:`CxEngineDedication`):
            api_version (str, optional):

        Returns:
            CxEngineServer

        Raises:
            BadRequestError
            NotFoundError
            CxError
        """
        result = None
        if dedications:
            if not isinstance(dedications, list):
                raise ValueError(
                    "parameter dedications should be a list of CxEngineDedication"
                )
            for dedication in dedications:
                if dedication and not isinstance(dedication, CxEngineDedication):
                    raise ValueError(
                        "member of dedications should be CxEngineDedication"
                    )

        post_data = json.dumps(
            {
                "dedications": (
                    [item.to_dict() for item in dedications] if dedications else []
                ),
                "name": name,
                "uri": uri,
                "minLoc": min_loc,
                "maxLoc": max_loc,
                "isBlocked": is_blocked,
                "maxScans": max_scans,
            }
        )
        url = f"{self.base_url}/cxrestapi/sast/engineServers"
        response = self.api_client.call_api(
            "POST", url, data=post_data, headers=get_headers(api_version)
        )
        if response.status_code == CREATED:
            result = CxEngineServer.from_dict(response.json())
        return result

    def unregister_engine_by_engine_id(
        self, engine_id: int, api_version: str = "5.0"
    ) -> bool:
        """
        DELETE /sast/engineServers/{id} Unregister an existing engine server.

        Args:
            engine_id (int): Unique Id of the engine server
            api_version (str, optional):

        Returns:
            boolean

        Raises:
            BadRequestError
            NotFoundError
            CxError
        """
        url = f"{self.base_url}/cxrestapi/sast/engineServers/{engine_id}"
        response = self.api_client.call_api(
            "DELETE", url, headers=get_headers(api_version)
        )
        return response.status_code == NO_CONTENT

    def get_engine_details(
        self, engine_id: int, api_version: str = "5.0"
    ) -> CxEngineServer:
        """
        GET /sast/engineServers/{id} Get details of a specific engine server by Id.

        Args:
            engine_id (int): Unique Id of the engine server
            api_version (str, optional):

        Returns:
            :obj:`CxEngineServer`

        Raises:
            BadRequestError
            NotFoundError
            CxError
        """
        result = None
        url = f"{self.base_url}/cxrestapi/sast/engineServers/{engine_id}"
        response = self.api_client.call_api(
            "GET", url, headers=get_headers(api_version)
        )
        if response.status_code == OK:
            result = CxEngineServer.from_dict(response.json())
        return result

    def update_engine_server(
        self,
        engine_id: int,
        name: str,
        uri: str,
        min_loc: int,
        max_loc: int,
        is_blocked: bool,
        max_scans: int = None,
        dedications: List[CxEngineDedication] = None,
        api_version: str = "5.0",
    ) -> CxEngineServer:
        """
        PUT /sast/engineServers/{id}  Update an existing engine server's configuration
                                        and enables to change certain parameters.


        Args:
            engine_id (int): Unique Id of the engine server
            name (str): Name of the engine server
            uri (str): Specifies the url of the engine server
            min_loc (int): Specifies the minimum number of lines of code to scan
            max_loc (int): Specifies the maximum number of lines of code to scan
            is_blocked (boolean): Specifies whether or not the engine will be able to receive scan requests
            max_scans (int): Specifies the maximum number of concurrent scans to perform
            dedications (`list` of :obj:`CxEngineDedication`):
            api_version (str, optional):

        Returns:
            CxEngineServer

        Raises:
            BadRequestError
            NotFoundError
            CxError
        """
        result = None
        if dedications:
            if not isinstance(dedications, list):
                raise ValueError(
                    "parameter dedications should be a list of CxEngineDedication"
                )
            for dedication in dedications:
                if dedication and not isinstance(dedication, CxEngineDedication):
                    raise ValueError(
                        "member of dedications should be CxEngineDedication"
                    )
        url = f"{self.base_url}/cxrestapi/sast/engineServers/{engine_id}"
        put_data = json.dumps(
            {
                "dedications": (
                    [item.to_dict() for item in dedications] if dedications else []
                ),
                "name": name,
                "uri": uri,
                "minLoc": min_loc,
                "maxLoc": max_loc,
                "isBlocked": is_blocked,
                "maxScans": max_scans,
            }
        )
        response = self.api_client.call_api(
            "PUT", url, data=put_data, headers=get_headers(api_version)
        )
        if response.status_code == OK:
            result = CxEngineServer.from_dict(response.json())
        return result

    def update_an_engine_server_by_edit_single_field(
        self,
        engine_id: int,
        name: str = None,
        uri: str = None,
        min_loc: int = None,
        max_loc: int = None,
        is_blocked: bool = None,
        max_scans: int = None,
        dedications: List[CxEngineDedication] = None,
        api_version: str = "5.0",
    ) -> bool:
        """
        PATCH  sast/engineServers/{id}
        Args:
            engine_id (int): Unique Id of the engine server
            name (str): Name of the engine server
            uri (str): Specifies the url of the engine server
            min_loc (int): Specifies the minimum number of lines of code to scan
            max_loc (int): Specifies the maximum number of lines of code to scan
            is_blocked (boolean): Specifies whether or not the engine will be able to receive scan requests
            max_scans (int): Specifies the maximum number of concurrent scans to perform
            dedications (`list` of :obj:`CxEngineDedication`):
            api_version (str, optional):

        Returns:
            is_successful (bool)

        Raises:
            BadRequestError
            NotFoundError
            CxError
        """
        if dedications:
            if not isinstance(dedications, list):
                raise ValueError(
                    "parameter dedications should be a list of CxEngineDedication"
                )
            for dedication in dedications:
                if dedication and not isinstance(dedication, CxEngineDedication):
                    raise ValueError(
                        "member of dedications should be CxEngineDedication"
                    )
        url = f"{self.base_url}/cxrestapi/sast/engineServers/{engine_id}"
        data = {}
        if name:
            data.update({"name": name})
        if uri:
            data.update({"uri": uri})
        if min_loc:
            data.update({"minLoc": min_loc})
        if max_loc:
            data.update({"maxLoc": max_loc})
        if is_blocked:
            data.update({"isBlocked": is_blocked})
        if max_scans:
            data.update({"maxScans": max_scans})
        if dedications:
            data.update({"dedications": [item.to_dict() for item in dedications]})
        patch_data = json.dumps(data)
        response = self.api_client.call_api(
            "PATCH", url, data=patch_data, headers=get_headers(api_version)
        )
        return response.status_code == NO_CONTENT

    def get_all_engine_configurations(
        self, api_version: str = "1.0"
    ) -> List[CxEngineConfiguration]:
        """
        GET /sast/engineConfigurations Get the engine servers configuration list.

        Args:
            api_version (str, optional):

        Returns:
            :obj:`list` of :obj:`CxEngineConfiguration`

        Raises:
            BadRequestError
            NotFoundError
            CxError

        """
        result = []
        url = f"{self.base_url}/cxrestapi/sast/engineConfigurations"
        response = self.api_client.call_api(
            "GET", url, headers=get_headers(api_version)
        )
        if response.status_code == OK:
            result = [CxEngineConfiguration.from_dict(item) for item in response.json()]
        return result

    def get_engine_configuration_id_by_name(
        self, engine_configuration_name: str
    ) -> int:
        """

        Args:
            engine_configuration_name (str):

        Returns:
            int: engine configuration id
        """
        all_engine_configurations = self.get_all_engine_configurations()
        a_dict = {item.name: item.id for item in all_engine_configurations}
        return a_dict.get(engine_configuration_name)

    def get_engine_configuration_by_id(
        self, configuration_id: int, api_version: str = "1.0"
    ) -> CxEngineConfiguration:
        """
        GET /sast/engineConfigurations/{id} Get a specific engine configuration by configuration Id.

        Args:
            configuration_id (int): Unique Id of the engine configuration
            api_version (str, optional):

        Returns:
            :obj:`CxEngineConfiguration`

        Raises:
            BadRequestError
            NotFoundError
            CxError
        """
        result = None
        url = f"{self.base_url}/cxrestapi/sast/engineConfigurations/{configuration_id}"
        response = self.api_client.call_api(
            "GET", url, headers=get_headers(api_version)
        )
        if response.status_code == OK:
            result = CxEngineConfiguration.from_dict(response.json())
        return result
