# encoding: utf-8

import json


class CxCreateScanSettingsRequestBody(object):
    """
    create scan settings
    """
    def __init__(self, project_id, preset_id, engine_configuration_id, post_scan_action_id=None,
                 failed_scan_emails=None, before_scan_emails=None, after_scan_emails=None):
        """

        :param project_id: int
        :param preset_id: int
        :param engine_configuration_id: int
        :param post_scan_action_id: int
        :param failed_scan_emails: list of str
        :param before_scan_emails: list of str
        :param after_scan_emails: list of str
        """
        self.project_id = project_id
        self.preset_id = preset_id
        self.engine_configuration_id = engine_configuration_id
        self.post_scan_action_id = post_scan_action_id
        self.failed_scan_emails = failed_scan_emails
        self.before_scan_emails = before_scan_emails
        self.after_scan_emails = after_scan_emails

    def get_post_data(self):
        return json.dumps(
            {
                "projectId": self.project_id,
                "presetId": self.preset_id,
                "engineConfigurationId": self.engine_configuration_id,
                "postScanActionId": self.post_scan_action_id,
                "emailNotifications": {
                    "failedScan": self.failed_scan_emails,
                    "beforeScan": self.before_scan_emails,
                    "afterScan": self.after_scan_emails
                }
            }
        )
