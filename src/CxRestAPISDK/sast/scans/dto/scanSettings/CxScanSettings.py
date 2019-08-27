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

        Args:
            project (:obj:`CxProject`):
            preset (:obj:`CxPreset`):
            engine_configuration (:obj:`CxEngineConfiguration`):
            post_scan_action (:obj:`CxCustomTask`):
            email_notifications (:obj:`CxEmailNotification`):
        """
        self.project = project
        self.preset = preset
        self.engine_configuration = engine_configuration
        self.post_scan_action = post_scan_action
        self.email_notification = email_notifications

    def __str__(self):
        return """CxScanSettings(project={}, preset={}, engine_configuration={}, 
            post_scan_action={}, email_notifications={})""".format(
            self.project, self.preset, self.engine_configuration, self.post_scan_action, self.email_notification
        )
