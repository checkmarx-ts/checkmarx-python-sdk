# encoding: utf-8
import json


class CxUpdateProjectRequest(object):
    """
    the request body of update project
    """

    def __init__(self, name, team_id, custom_fields):
        """

        Args:
            name (str):  the project name that you want the current project change to
            owning_team（int):  the team id that you want the current project change to
            custom_fields (:obj:`list` of :obj:`CxCustomField`):
        """
        self.name = name
        self.owning_team = team_id
        self.custom_fields = custom_fields

    def get_post_data(self):
        """
        the data of post http request body
        :return:
        dict

        """
        if self.custom_fields:
            custom_fields = [{'id': cf.id, 'value': cf.value} for cf in self.custom_fields]
        else:
            custom_fields = []
        return json.dumps(
            {
                "name": self.name,
                "owningTeam": self.owning_team,
                "customFields": custom_fields
            }
        )

    def __str__(self):
        return "CxUpdateProjectRequest(name={}, owning_team={}, custom_fields={})".format(
            self.name, self.owning_team, self.custom_fields
        )
