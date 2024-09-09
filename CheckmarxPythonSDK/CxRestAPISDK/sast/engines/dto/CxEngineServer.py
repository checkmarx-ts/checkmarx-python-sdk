# encoding: utf-8
from .CxEngineDedication import CxEngineDedication


class CxEngineServer(object):
    """
    engine server
    """

    def __init__(self, engine_server_id=None, name=None, uri=None, min_loc=None, max_loc=None, max_scans=None,
                 cx_version=None, operating_system=None, status=None, link=None, offline_reason_code=None,
                 offline_reason_message=None, offline_reason_message_parameters=None, dedications=None):
        """

        Args:
            engine_server_id (int):
            name (str):
            uri (str):
            min_loc (int):
            max_loc (int):
            max_scans (int):
            cx_version (str):
            operating_system (str):
            status (:obj:`CxEngineServerStatus`): ['Offline', 'Blocked', 'ScanningAndBlocked', 'Scanning', 'Idle']
            link (:obj:`CxLink`):
            offline_reason_code (str):  ['Online', 'CannotAccess', 'EngineServerError',
                'MessageQueueConfigurationIssue', 'OnlineButMessageQueueConfigurationValidatationError',
                'ActiveMQConnectionError', 'EngineAndPackVersionMismtach', 'EngineDiskSpaceError'],
            offline_reason_message (str):
            offline_reason_message_parameters (str):
            dedications (`list` of :obj:`CxEngineDedication`)
        """
        if dedications:
            if not isinstance(dedications, list):
                raise ValueError("parameter dedications should be a list of CxEngineDedication")
            for item in dedications:
                if item and not isinstance(item, CxEngineDedication):
                    raise ValueError("member of dedications should be CxEngineDedication")

        self.id = engine_server_id
        self.name = name
        self.uri = uri
        self.min_loc = min_loc
        self.max_loc = max_loc
        self.max_scans = max_scans
        self.cx_version = cx_version
        self.operating_system = operating_system
        self.status = status
        self.link = link
        self.offline_reason_code = offline_reason_code
        self.offline_reason_message = offline_reason_message
        self.offline_reason_message_parameters = offline_reason_message_parameters
        self.dedications = dedications

    def __str__(self):
        return """CxEngineServer(id={}, name={}, uri={}, min_loc={}, max_loc={}, max_scans={}, 
                 cx_version={}, operating_system={}, status={}, link={}, 
                 offline_reason_code={}, offline_reason_message={}, 
                 offline_reason_message_parameters={}, dedications={})""".format(
            self.id, self.name, self.uri, self.min_loc, self.max_loc, self.max_scans,
            self.cx_version, self.operating_system, self.status, self.link,
            self.offline_reason_code, self.offline_reason_message, self.offline_reason_message_parameters,
            self.dedications
        )
