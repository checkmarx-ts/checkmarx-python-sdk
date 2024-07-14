# encoding: utf-8


class CxScanSettings(object):
    """
    scan settings
    """

    def __init__(self, project, preset, engine_configuration, post_scan_action, email_notifications,
                 post_scan_action_data=None, post_scan_action_name=None, post_scan_action_conditions=None,
                 post_scan_action_arguments=None):
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
            post_scan_action_data (str):
            post_scan_action_name (str):
            post_scan_action_conditions (:obj:`CxPostScanActionConditions`):
            post_scan_action_arguments (str):

        """
        self.project = project
        self.preset = preset
        self.engine_configuration = engine_configuration
        self.post_scan_action = post_scan_action
        self.email_notification = email_notifications
        self.post_scan_action_data = post_scan_action_data
        self.post_scan_action_name = post_scan_action_name
        self.post_scan_action_conditions = post_scan_action_conditions
        self.post_scan_action_arguments = post_scan_action_arguments

    def __str__(self):
        return """CxScanSettings(project={}, preset={}, engine_configuration={}, 
            post_scan_action={}, email_notifications={}, post_scan_action_data={}, post_scan_action_name={},
            post_scan_action_conditions={}, post_scan_action_arguments={})""".format(
            self.project, self.preset, self.engine_configuration, self.post_scan_action, self.email_notification,
            self.post_scan_action_data, self.post_scan_action_name, self.post_scan_action_conditions,
            self.post_scan_action_arguments
        )
