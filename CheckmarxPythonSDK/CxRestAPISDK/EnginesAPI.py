# encoding: utf-8
import json
from .httpRequests import get_request, post_request, put_request, patch_request, delete_request, get_headers
from CheckmarxPythonSDK.utilities.compat import OK, NO_CONTENT, CREATED
from .sast.projects.dto import CxLink
from .sast.engines.dto import (CxEngineServer, CxEngineConfiguration, CxEngineServerStatus)


class EnginesAPI(object):
    """
    engines API
    """
    @staticmethod
    def get_all_engine_server_details(api_version="1.0"):
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
        response = get_request(relative_url=relative_url, headers=get_headers(api_version))
        if response.status_code == OK:
            result = [
                CxEngineServer(
                    engine_server_id=item.get("id"),
                    name=item.get("name"),
                    uri=item.get("uri"),
                    min_loc=item.get("minLoc"),
                    max_loc=item.get("maxLoc"),
                    max_scans=item.get("maxScans"),
                    cx_version=item.get("cxVersion"),
                    status=CxEngineServerStatus(
                        status_id=(item.get("status", {}) or {}).get("id"),
                        value=(item.get("status", {}) or {}).get("value"),
                    ),
                    link=CxLink(
                        rel=(item.get("link", {}) or {}).get("rel"),
                        uri=(item.get("link", {}) or {}).get("uri")
                    )
                ) for item in response.json()
            ]
        return result

    @staticmethod
    def get_engine_id_by_name(engine_name):
        """

        Args:
            engine_name (str):

        Returns:
            int: engine id
        """
        all_engine_servers = EnginesAPI.get_all_engine_server_details()
        a_dict = {item.name: item.id for item in all_engine_servers}
        return a_dict.get(engine_name)

    @staticmethod
    def register_engine(name, uri, min_loc, max_loc, is_blocked, max_scans, api_version="1.0"):
        """
        POST  /sast/engineServers  Registers an Engine Server
        Args:
            name (str): Name of the engine server
            uri (str): Specifies the url of the engine server
            min_loc (int): Specifies the minimum number of lines of code to scan
            max_loc (int): Specifies the maximum number of lines of code to scan
            is_blocked (boolean): Specifies whether or not the engine will be able to receive scan requests
            max_scans (int):
            api_version (str, optional):

        Returns:
            CxEngineServer

        Raises:
            BadRequestError
            NotFoundError
            CxError
        """
        result = None
        post_data = json.dumps(
            {
                "name": name,
                "uri": uri,
                "minLoc": min_loc,
                "maxLoc": max_loc,
                "isBlocked": is_blocked,
                "maxScans": max_scans
            }
        )
        relative_url = "/cxrestapi/sast/engineServers"
        response = post_request(relative_url=relative_url, data=post_data, headers=get_headers(api_version))
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

    @staticmethod
    def unregister_engine_by_engine_id(engine_id, api_version="1.0"):
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
        result = False
        relative_url = "/cxrestapi/sast/engineServers/{id}".format(id=engine_id)
        response = delete_request(relative_url=relative_url, headers=get_headers(api_version))
        if response.status_code == NO_CONTENT:
            result = True
        return result

    @staticmethod
    def get_engine_details(engine_id, api_version="1.0"):
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
        response = get_request(relative_url=relative_url, headers=get_headers(api_version))
        if response.status_code == OK:
            item = response.json()
            result = CxEngineServer(
                engine_server_id=item.get("id"),
                name=item.get("name"),
                uri=item.get("uri"),
                min_loc=item.get("minLoc"),
                max_loc=item.get("maxLoc"),
                max_scans=item.get("maxScans"),
                cx_version=item.get("cxVersion"),
                status=CxEngineServerStatus(
                    status_id=(item.get("status", {}) or {}).get("id"),
                    value=(item.get("status", {}) or {}).get("value"),
                ),
                link=CxLink(
                    rel=(item.get("link", {}) or {}).get("rel"),
                    uri=(item.get("link", {}) or {}).get("uri")
                )
            )
        return result

    @staticmethod
    def update_engine_server(engine_id, name, uri, min_loc, max_loc, is_blocked, max_scans=None,
                             api_version="1.0"):
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
            api_version (str, optional):

        Returns:
            CxEngineServer

        Raises:
            BadRequestError
            NotFoundError
            CxError
        """
        result = None
        relative_url = "/cxrestapi/sast/engineServers/{id}".format(id=engine_id)
        put_data = json.dumps(
            {
                "name": name,
                "uri": uri,
                "minLoc": min_loc,
                "maxLoc": max_loc,
                "isBlocked": is_blocked,
                "maxScans": max_scans
            }
        )
        response = put_request(relative_url=relative_url, data=put_data, headers=get_headers(api_version))
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

    @staticmethod
    def update_an_engine_server_by_edit_single_field(engine_id, name, uri, min_loc, max_loc, is_blocked,
                                                     max_scans, api_version="1.0"):
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
            api_version (str, optional):

        Returns:
            is_successful (bool)

        Raises:
            BadRequestError
            NotFoundError
            CxError
        """
        result = False
        relative_url = "/cxrestapi/sast/engineServers/{id}".format(id=engine_id)
        patch_data = json.dumps(
            {
                "name": name,
                "uri": uri,
                "minLoc": min_loc,
                "maxLoc": max_loc,
                "isBlocked": is_blocked,
                "maxScans": max_scans
            }
        )
        response = patch_request(relative_url=relative_url, data=patch_data, headers=get_headers(api_version))
        if response.status_code == NO_CONTENT:
            result = True
        return result

    @staticmethod
    def get_all_engine_configurations(api_version="1.0"):
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
        response = get_request(relative_url=relative_url, headers=get_headers(api_version))
        if response.status_code == OK:
            result = [
                CxEngineConfiguration(
                    engine_configuration_id=item.get("id"),
                    name=item.get("name")
                ) for item in response.json()
            ]
        return result

    @staticmethod
    def get_engine_configuration_id_by_name(engine_configuration_name):
        """

        Args:
            engine_configuration_name (str):

        Returns:
            int: engine configuration id
        """
        all_engine_configurations = EnginesAPI.get_all_engine_configurations()
        a_dict = {item.name: item.id for item in all_engine_configurations}
        return a_dict.get(engine_configuration_name)

    @staticmethod
    def get_engine_configuration_by_id(configuration_id, api_version="1.0"):
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
        response = get_request(relative_url=relative_url, headers=get_headers(api_version))
        if response.status_code == OK:
            a_dict = response.json()
            result = CxEngineConfiguration(
                engine_configuration_id=a_dict.get("id"),
                name=a_dict.get("name")
            )
        return result
