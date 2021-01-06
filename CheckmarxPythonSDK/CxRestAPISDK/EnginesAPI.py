# encoding: utf-8

import requests

from ..compat import OK, BAD_REQUEST, NOT_FOUND, UNAUTHORIZED, NO_CONTENT, CREATED
from ..config import config

from . import authHeaders
from .exceptions.CxError import BadRequestError, NotFoundError, CxError
from .sast.projects.dto import CxLink
from .sast.engines.dto import (CxRegisterEngineRequestBody, CxEngineServer, CxEngineConfiguration, CxEngineServerStatus)


class EnginesAPI(object):
    """
    engines API
    """

    def __init__(self):
        self.retry = 0

    def get_all_engine_server_details(self):
        """

        Returns:
            :obj:`CxEngineServer`

        Raises:
            BadRequestError
            NotFoundError
            CxError
        """
        all_engine_server_details = None

        engine_servers_url = config.get("base_url") + "/cxrestapi/sast/engineServers"

        r = requests.get(
            url=engine_servers_url,
            headers=authHeaders.auth_headers,
            verify=config.get("verify")
        )
        if r.status_code == OK:
            a_list = r.json()
            all_engine_server_details = [
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
                ) for item in a_list
            ]
        elif r.status_code == BAD_REQUEST:
            raise BadRequestError(r.text)
        elif r.status_code == NOT_FOUND:
            raise NotFoundError()
        elif (r.status_code == UNAUTHORIZED) and (self.retry < config.get("max_try")):
            authHeaders.update_auth_headers()
            self.retry += 1
            self.get_all_engine_server_details()
        else:
            raise CxError(r.text, r.status_code)

        self.retry = 0

        return all_engine_server_details

    def get_engine_id_by_name(self, engine_name):
        """

        Args:
            engine_name (str):

        Returns:
            int: engine id
        """
        all_engine_servers = self.get_all_engine_server_details()
        a_dict = {item.name: item.id for item in all_engine_servers}
        return a_dict.get(engine_name)

    def register_engine(self, name, uri, min_loc, max_loc, is_blocked):
        """

        Args:
            name (str): Name of the engine server
            uri (str): Specifies the url of the engine server
            min_loc (int): Specifies the minimum number of lines of code to scan
            max_loc (int): Specifies the maximum number of lines of code to scan
            is_blocked (boolean): Specifies whether or not the engine will be able to receive scan requests

        Returns:
            CxEngineServer

        Raises:
            BadRequestError
            NotFoundError
            CxError
        """
        engine_server = None

        post_request_body = CxRegisterEngineRequestBody(
            name=name,
            uri=uri,
            min_loc=min_loc,
            max_loc=max_loc,
            is_blocked=is_blocked
        ).get_post_data()

        engine_servers_url = config.get("base_url") + "/cxrestapi/sast/engineServers"

        r = requests.post(
            engine_servers_url,
            data=post_request_body,
            headers=authHeaders.auth_headers,
            verify=config.get("verify")
        )

        if r.status_code == CREATED:
            a_dict = r.json()
            engine_server = CxEngineServer(
                engine_server_id=a_dict.get("id"),
                link=CxLink(
                    rel=(a_dict.get("link", {}) or {}).get("rel"),
                    uri=(a_dict.get("link", {}) or {}).get("uri")
                )
            )
        elif r.status_code == BAD_REQUEST:
            raise BadRequestError(r.text)
        elif r.status_code == NOT_FOUND:
            raise NotFoundError()
        elif (r.status_code == UNAUTHORIZED) and (self.retry < config.get("max_try")):
            authHeaders.update_auth_headers()
            self.retry += 1
            self.register_engine(name, uri, min_loc, max_loc, is_blocked)
        else:
            raise CxError(r.text, r.status_code)

        self.retry = 0

        return engine_server

    def unregister_engine_by_engine_id(self, engine_id):
        """
        Unregister an existing engine server.

        Args:
            engine_id (int): Unique Id of the engine server

        Returns:
            boolean

        Raises:
            BadRequestError
            NotFoundError
            CxError
        """
        is_successful = False

        engine_server_url = config.get("base_url") + "/cxrestapi/sast/engineServers/{id}".format(id=engine_id)

        r = requests.delete(
            url=engine_server_url,
            headers=authHeaders.auth_headers,
            verify=config.get("verify")
        )

        if r.status_code == NO_CONTENT:
            is_successful = True
        elif r.status_code == BAD_REQUEST:
            raise BadRequestError(r.text)
        elif r.status_code == NOT_FOUND:
            raise NotFoundError()
        elif (r.status_code == UNAUTHORIZED) and (self.retry < config.get("max_try")):
            authHeaders.update_auth_headers()
            self.retry += 1
            self.unregister_engine_by_engine_id(engine_id)
        else:
            raise CxError(r.text, r.status_code)

        self.retry = 0

        return is_successful

    def get_engine_details(self, engine_id):
        """
        Get details of a specific engine server by Id.

        Args:
            engine_id (int): Unique Id of the engine server

        Returns:
            :obj:`CxEngineServer`

        Raises:
            BadRequestError
            NotFoundError
            CxError
        """
        engine_server = None

        engine_server_url = config.get("base_url") + "/cxrestapi/sast/engineServers/{id}".format(id=engine_id)

        r = requests.get(
            url=engine_server_url,
            headers=authHeaders.auth_headers,
            verify=config.get("verify")
        )
        if r.status_code == OK:
            item = r.json()
            engine_server = CxEngineServer(
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
        elif r.status_code == BAD_REQUEST:
            raise BadRequestError(r.text)
        elif r.status_code == NOT_FOUND:
            raise NotFoundError()
        elif (r.status_code == UNAUTHORIZED) and (self.retry < config.get("max_try")):
            authHeaders.update_auth_headers()
            self.retry += 1
            self.get_engine_details(engine_id)
        else:
            raise CxError(r.text, r.status_code)

        self.retry = 0

        return engine_server

    def update_engine_server(self, engine_id, name, uri, min_loc, max_loc, is_blocked, max_scans=None):
        """
        Update an existing engine server's configuration and enables to change certain parameters.


        Args:
            engine_id (int): Unique Id of the engine server
            name (str): Name of the engine server
            uri (str): Specifies the url of the engine server
            min_loc (int): Specifies the minimum number of lines of code to scan
            max_loc (int): Specifies the maximum number of lines of code to scan
            is_blocked (boolean): Specifies whether or not the engine will be able to receive scan requests
            max_scans (int): Specifies the maximum number of concurrent scans to perform

        Returns:
            CxEngineServer

        Raises:
            BadRequestError
            NotFoundError
            CxError
        """
        engine_server = None

        engine_server_url = config.get("base_url") + "/cxrestapi/sast/engineServers/{id}".format(id=engine_id)

        data = CxRegisterEngineRequestBody(
            name=name,
            uri=uri,
            min_loc=min_loc,
            max_loc=max_loc,
            is_blocked=is_blocked,
            max_scans=max_scans
        ).get_post_data()

        r = requests.put(
            url=engine_server_url,
            data=data,
            headers=authHeaders.auth_headers,
            verify=config.get("verify")
        )

        if r.status_code == OK:
            a_dict = r.json()
            engine_server = CxEngineServer(
                engine_server_id=a_dict.get("id"),
                link=CxLink(
                    rel=(a_dict.get("link", {}) or {}).get("rel"),
                    uri=(a_dict.get("link", {}) or {}).get("uri")
                )
            )
        elif r.status_code == BAD_REQUEST:
            raise BadRequestError(r.text)
        elif r.status_code == NOT_FOUND:
            raise NotFoundError()
        elif (r.status_code == UNAUTHORIZED) and (self.retry < config.get("max_try")):
            authHeaders.update_auth_headers()
            self.retry += 1
            self.update_engine_server(engine_id, name, uri, min_loc, max_loc, is_blocked, max_scans)
        else:
            raise CxError(r.text, r.status_code)

        self.retry = 0

        return engine_server

    def get_all_engine_configurations(self):
        """
        Get the engine servers configuration list.

        Returns:
            :obj:`list` of :obj:`CxEngineConfiguration`

        Raises:
            BadRequestError
            NotFoundError
            CxError

        """
        all_engine_configurations = None

        engine_configurations_url = config.get("base_url") + "/cxrestapi/sast/engineConfigurations"

        r = requests.get(
            url=engine_configurations_url,
            headers=authHeaders.auth_headers,
            verify=config.get("verify")
        )
        if r.status_code == OK:
            a_list = r.json()
            all_engine_configurations = [
                CxEngineConfiguration(
                    engine_configuration_id=item.get("id"),
                    name=item.get("name")
                ) for item in a_list
            ]
        elif r.status_code == BAD_REQUEST:
            raise BadRequestError(r.text)
        elif r.status_code == NOT_FOUND:
            raise NotFoundError()
        elif (r.status_code == UNAUTHORIZED) and (self.retry < config.get("max_try")):
            authHeaders.update_auth_headers()
            self.retry += 1
            self.get_all_engine_configurations()
        else:
            raise CxError(r.text, r.status_code)

        self.retry = 0

        return all_engine_configurations

    def get_engine_configuration_id_by_name(self, engine_configuration_name):
        """

        Args:
            engine_configuration_name (str):

        Returns:
            int: engine configuration id
        """
        all_engine_configurations = self.get_all_engine_configurations()
        a_dict = {item.name: item.id for item in all_engine_configurations}
        return a_dict.get(engine_configuration_name)

    def get_engine_configuration_by_id(self, configuration_id):
        """
        Get a specific engine configuration by configuration Id.

        Args:
            configuration_id (int): Unique Id of the engine configuration

        Returns:
            :obj:`CxEngineConfiguration`

        Raises:
            BadRequestError
            NotFoundError
            CxError
        """
        engine_configuration = None

        engine_configuration_url = config.get("base_url") + "/cxrestapi/sast/engineConfigurations/{id}".format(
            id=configuration_id
        )

        r = requests.get(
            url=engine_configuration_url,
            headers=authHeaders.auth_headers,
            verify=config.get("verify")
        )
        if r.status_code == OK:
            a_dict = r.json()
            engine_configuration = CxEngineConfiguration(
                engine_configuration_id=a_dict.get("id"),
                name=a_dict.get("name")
            )
        elif r.status_code == BAD_REQUEST:
            raise BadRequestError(r.text)
        elif r.status_code == NOT_FOUND:
            raise NotFoundError()
        elif (r.status_code == UNAUTHORIZED) and (self.retry < config.get("max_try")):
            authHeaders.update_auth_headers()
            self.retry += 1
            self.get_engine_configuration_by_id(configuration_id)
        else:
            raise CxError(r.text, r.status_code)

        self.retry = 0

        return engine_configuration
