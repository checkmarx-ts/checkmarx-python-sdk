# encoding: utf-8

import json


class CxCreateScanSettingsRequestBody(object):
    """
    create scan settings
    """
    def __init__(self, project_id, preset_id, engine_configuration_id, post_scan_action_id=None,
                 failed_scan_emails=None, before_scan_emails=None, after_scan_emails=None):
        """

        Args:
            project_id (int):
            preset_id (int):
            engine_configuration_id (int):
            post_scan_action_id (int): optional.
            failed_scan_emails (:obj:`list` of :obj:`str`): optional
            before_scan_emails (:obj:`list` of :obj:`str`): optional
            after_scan_emails (:obj:`list` of :obj:`str`): optional
        """
        self.project_id = project_id
        self.preset_id = preset_id
        self.engine_configuration_id = engine_configuration_id
        self.post_scan_action_id = post_scan_action_id
        self.failed_scan_emails = failed_scan_emails
        self.before_scan_emails = before_scan_emails
        self.after_scan_emails = after_scan_emails

    def get_post_data(self):
        target_dict = {
            "projectId": self.project_id,
            "presetId": self.preset_id,
            "engineConfigurationId": self.engine_configuration_id
        }

        if self.post_scan_action_id:
            target_dict.update({"postScanActionId": self.post_scan_action_id})

        emails_dict = dict()
        if self.failed_scan_emails:
            emails_dict.update({"failedScan": self.failed_scan_emails})
        if self.before_scan_emails:
            emails_dict.update({"beforeScan": self.before_scan_emails})
        if self.after_scan_emails:
            emails_dict.update({"afterScan": self.after_scan_emails})

        if self.failed_scan_emails or self.before_scan_emails or self.after_scan_emails:
            target_dict.update({"emailNotifications": emails_dict})

        return json.dumps(target_dict)

    def __str__(self):
        return """CxCreateScanSettingsRequestBody(
                    project_id={}, 
                    preset_id={}, 
                    engine_configuration_id={}, 
                    post_scan_action_id={}, 
                    failed_scan_emails={}, 
                    before_scan_emails={}, 
                    after_scan_emails={})""".format(
            self.project_id, self.preset_id, self.engine_configuration_id, self.post_scan_action_id,
            self.failed_scan_emails, self.before_scan_emails, self.after_scan_emails
        )
