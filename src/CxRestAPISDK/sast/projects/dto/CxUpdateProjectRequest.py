# encoding: utf-8
import json

from src.CxRestAPISDK.sast.projects.dto.customFields import CxCustomField


class CxUpdateProjectRequest(object):
    """
    the request body of update project
    """

    def __init__(self, name, owning_team, custom_field_id, custom_field_value):
        """

        Args:
            name (str):  the project name that you want the current project change to
            owning_team（int):  the team id that you want the current project change to
            custom_field_id （int): the id of the custom field that you want to change
            custom_field_value (str): the value of the custom field that you want to change to
        """
        self.name = name
        self.owning_team = owning_team
        self.custom_fields = CxCustomField.CxCustomField(custom_field_id=custom_field_id, name=custom_field_value)

    def get_post_data(self):
        """
        the data of post http request body
        :return:
        dict

        """
        return json.dumps(
            {
                "name": self.name,
                "owningTeam": self.owning_team,
                "customFields": [
                    {
                        "id": self.custom_fields.id,
                        "value": self.custom_fields.name
                    }
                ] if self.custom_fields else []
            }
        )

    def __str__(self):
        return "CxUpdateProjectRequest(name={}, owning_team={}, custom_fields={})".format(
            self.name, self.owning_team, self.custom_fields
        )
