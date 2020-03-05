# encoding: utf-8
import json


class CxIssueTrackingSystemJira(object):
    """
    issue tracking system jira
    """

    def __init__(self, issue_tracking_system_id, jira_project_id, issue_type_id, fields):
        """

        Args:
            issue_tracking_system_id (int):
            jira_project_id (str):
            issue_type_id (str):
            fields (:obj:`list` of :obj:`CxIssueTrackingSystemJiraField`):
        """
        self.issue_tracking_system_id = issue_tracking_system_id
        self.jira_project_id = jira_project_id
        self.issue_type_id = issue_type_id
        self.fields = fields

    def get_post_data(self):
        return json.dumps(
            {
                "issueTrackingSystemId": self.issue_tracking_system_id,
                "jiraProjectId": self.jira_project_id,
                "issueType": {
                    "id": self.issue_type_id,
                    "fields": [
                        {
                            "id": field.id,
                            "values": field.values
                        } for field in self.fields
                    ]
                }
            }
        )

    def __str__(self):
        return """CxIssueTrackingSystemJira(issue_tracking_system_id={}, jira_project_id={}, 
                issue_type_id={}, fields={})""".format(
            self.issue_tracking_system_id, self.jira_project_id, self.issue_type_id, self.fields
        )
