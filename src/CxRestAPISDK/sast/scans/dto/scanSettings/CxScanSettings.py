# encoding: utf-8


class CxScanSettings(object):
    """
    scan settings
    """

    def __init__(self, project, preset, engine_configuration, post_scan_action, email_notifications):
        """

        :param project:
        :param preset:
        :param engine_configuration:
        :param post_scan_action:
        :param email_notifications:
        """
        self.project = project
        self.preset = preset
        self.engine_configuration = engine_configuration
        self.post_scan_action = post_scan_action
        self.email_notification = email_notifications
