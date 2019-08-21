# encoding: utf-8
import json


class CxUpdateProjectNameTeamIdRequest(object):
    """
    the request body to update project name and team id
    """

    def __init__(self, project_name, owning_team):
        """

        :param project_name: str
        :param owning_team: int
            team_id
        """
        self.project_name = project_name
        self.owning_team = owning_team

    def get_post_data(self):
        """

        :return:
        """
        return json.dumps(
            {
                "name": self.project_name,
                "owningTeam": self.owning_team
            }
        )
