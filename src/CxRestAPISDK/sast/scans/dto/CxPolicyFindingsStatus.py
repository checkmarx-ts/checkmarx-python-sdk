# encoding: utf-8


class CxPolicyFindingsStatus(object):
    """
    policy finding status
    """
    def __init__(self, project=None, scan=None, status=None, last_sync=None):
        """

        :param project: CxProject
        :param scan: CxScan
        :param status: str
        :param last_sync: str
        """
        self.project = project
        self.scan = scan
        self.status = status
        self.last_sync = last_sync
