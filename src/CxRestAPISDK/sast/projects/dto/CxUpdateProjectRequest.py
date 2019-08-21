# encoding: utf-8
import json

from src.CxRestAPISDK.sast.projects.dto.customFields import CxCustomFields


class CxUpdateProjectRequest(object):
    """
    the request body of update project
    """

    def __init__(self, name, owning_team, custom_field_id, custom_field_value):
        """

        :param name: str
            the project name that you want the current project change to
        :param owning_team: int
            the team id that you want the current project change to
        :param custom_field_id:
            the id of the custom field that you want to change
        :param custom_field_value:
            the value of the custom field that you want to change to
        """
        self.name = name
        self.owning_team = owning_team
        if custom_field_id and custom_field_value:
            self.custom_fields = CxCustomFields.CxCustomFields(id=custom_field_id, name=custom_field_value)
        else:
            self.custom_fields = None

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
