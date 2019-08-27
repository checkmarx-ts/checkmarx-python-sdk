# encoding: utf-8


class CxPolicyFindingsStatus(object):
    """
    policy finding status
    """
    def __init__(self, project=None, scan=None, status=None, last_sync=None):
        """

        Args:
            project (:obj:`CxProject`):
            scan (:obj:`CxScan`):
            status (str):
            last_sync (str):
        """
        self.project = project
        self.scan = scan
        self.status = status
        self.last_sync = last_sync

    def __str__(self):
        return "CxPolicyFindingsStatus(project={}, scan={}, status={}, last_sync={})".format(
            self.project, self.scan, self.status, self.last_sync
        )
