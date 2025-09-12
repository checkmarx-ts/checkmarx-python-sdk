import json
from typing import List
from CheckmarxPythonSDK.api_client import ApiClient
from CheckmarxPythonSDK.CxRestAPISDK.config import construct_configuration, get_headers
from CheckmarxPythonSDK.utilities.compat import OK, NO_CONTENT, CREATED
from .sast.projects.dto import CxLink
from .sast.engines.dto import (CxEngineServer, CxEngineConfiguration, CxEngineDedication, CxEngineServerStatus)


def construct_engine_server(item):
    return CxEngineServer(
        engine_server_id=item.get("id"),
        name=item.get("name"),
        uri=item.get("uri"),
        min_loc=item.get("minLoc"),
        max_loc=item.get("maxLoc"),
        max_scans=item.get("maxScans"),
        cx_version=item.get("cxVersion"),
        operating_system=item.get("operatingSystem"),
        status=CxEngineServerStatus(
            status_id=(item.get("status", {}) or {}).get("id"),
            value=(item.get("status", {}) or {}).get("value"),
        ),
        link=CxLink(
            rel=(item.get("link", {}) or {}).get("rel"),
            uri=(item.get("link", {}) or {}).get("uri")
        ),
        offline_reason_code=item.get("offlineReasonCode"),
        offline_reason_message=item.get("offlineReasonMessage"),
        offline_reason_message_parameters=item.get("offlineReasonMessageParameters"),
        dedications=[
            CxEngineDedication(
                item_type=va.get("itemType"),
                item_id=va.get("itemId"),
                item_name=va.get("itemName"),
            ) for va in item.get("dedications", [{}])
        ]
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

    def get_all_engine_server_details(self, api_version: str = "5.0") -> List[CxEngineServer]:
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
        relative_url = "/cxrestapi/sast/engineServers"
        response = self.api_client.get_request(relative_url=relative_url, headers=get_headers(api_version))
        if response.status_code == OK:
            result = [
                construct_engine_server(item) for item in response.json()
            ]
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
            self, name: str, uri: str, min_loc: int, max_loc: int, is_blocked: bool,
            max_scans: int, dedications: List[CxEngineDedication] = None, api_version: str = "5.0"
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
                raise ValueError("parameter dedications should be a list of CxEngineDedication")
            for dedication in dedications:
                if dedication and not isinstance(dedication, CxEngineDedication):
                    raise ValueError("member of dedications should be CxEngineDedication")

        post_data = json.dumps(
            {
                "dedications": [
                    item.to_dict() for item in dedications
                ],
                "name": name,
                "uri": uri,
                "minLoc": min_loc,
                "maxLoc": max_loc,
                "isBlocked": is_blocked,
                "maxScans": max_scans
            }
        )
        relative_url = "/cxrestapi/sast/engineServers"
        response = self.api_client.post_request(
            relative_url=relative_url, data=post_data, headers=get_headers(api_version))
        if response.status_code == CREATED:
            a_dict = response.json()
            result = CxEngineServer(
                engine_server_id=a_dict.get("id"),
                link=CxLink(
                    rel=(a_dict.get("link", {}) or {}).get("rel"),
                    uri=(a_dict.get("link", {}) or {}).get("uri")
                )
            )
        return result

    def unregister_engine_by_engine_id(self, engine_id: int, api_version: str = "5.0") -> bool:
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
        relative_url = "/cxrestapi/sast/engineServers/{id}".format(id=engine_id)
        response = self.api_client.delete_request(relative_url=relative_url, headers=get_headers(api_version))
        return response.status_code == NO_CONTENT

    def get_engine_details(self, engine_id: int, api_version: str = "5.0") -> CxEngineServer:
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
        relative_url = "/cxrestapi/sast/engineServers/{id}".format(id=engine_id)
        response = self.api_client.get_request(relative_url=relative_url, headers=get_headers(api_version))
        if response.status_code == OK:
            item = response.json()
            result = construct_engine_server(item)
        return result

    def update_engine_server(
            self, engine_id: int, name: str, uri: str, min_loc: int, max_loc: int, is_blocked: bool,
            max_scans: int = None, dedications: List[CxEngineDedication] = None,
            api_version: str = "5.0"
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
                raise ValueError("parameter dedications should be a list of CxEngineDedication")
            for dedication in dedications:
                if dedication and not isinstance(dedication, CxEngineDedication):
                    raise ValueError("member of dedications should be CxEngineDedication")
        relative_url = "/cxrestapi/sast/engineServers/{id}".format(id=engine_id)
        put_data = json.dumps(
            {
                "dedications": [
                    item.to_dict() for item in dedications
                ],
                "name": name,
                "uri": uri,
                "minLoc": min_loc,
                "maxLoc": max_loc,
                "isBlocked": is_blocked,
                "maxScans": max_scans
            }
        )
        response = self.api_client.put_request(
            relative_url=relative_url, data=put_data, headers=get_headers(api_version))
        if response.status_code == OK:
            a_dict = response.json()
            result = CxEngineServer(
                engine_server_id=a_dict.get("id"),
                link=CxLink(
                    rel=(a_dict.get("link", {}) or {}).get("rel"),
                    uri=(a_dict.get("link", {}) or {}).get("uri")
                )
            )
        return result

    def update_an_engine_server_by_edit_single_field(
            self, engine_id: int, name: str = None, uri: str = None, min_loc: int = None, max_loc: int = None,
            is_blocked: bool = None, max_scans: int = None, dedications: List[CxEngineDedication] = None,
            api_version: str = "5.0"
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
                raise ValueError("parameter dedications should be a list of CxEngineDedication")
            for dedication in dedications:
                if dedication and not isinstance(dedication, CxEngineDedication):
                    raise ValueError("member of dedications should be CxEngineDedication")
        relative_url = "/cxrestapi/sast/engineServers/{id}".format(id=engine_id)
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
            data.update({"dedications": [
                    item.to_dict() for item in dedications
                ]})
        patch_data = json.dumps(data)
        response = self.api_client.patch_request(
            relative_url=relative_url, data=patch_data, headers=get_headers(api_version))
        return response.status_code == NO_CONTENT

    def get_all_engine_configurations(self, api_version: str = "1.0") -> List[CxEngineConfiguration]:
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
        relative_url = "/cxrestapi/sast/engineConfigurations"
        response = self.api_client.get_request(relative_url=relative_url, headers=get_headers(api_version))
        if response.status_code == OK:
            result = [
                CxEngineConfiguration(
                    engine_configuration_id=item.get("id"),
                    name=item.get("name")
                ) for item in response.json()
            ]
        return result

    def get_engine_configuration_id_by_name(self, engine_configuration_name: str) -> int:
        """

        Args:
            engine_configuration_name (str):

        Returns:
            int: engine configuration id
        """
        all_engine_configurations = self.get_all_engine_configurations()
        a_dict = {item.name: item.id for item in all_engine_configurations}
        return a_dict.get(engine_configuration_name)

    def get_engine_configuration_by_id(self, configuration_id: int, api_version: str = "1.0") -> CxEngineConfiguration:
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
        relative_url = "/cxrestapi/sast/engineConfigurations/{id}".format(id=configuration_id)
        response = self.api_client.get_request(relative_url=relative_url, headers=get_headers(api_version))
        if response.status_code == OK:
            a_dict = response.json()
            result = CxEngineConfiguration(
                engine_configuration_id=a_dict.get("id"),
                name=a_dict.get("name")
            )
        return result
