# encoding: utf-8
import json


class CxUpdateProjectNameTeamIdRequest(object):
    """
    the request body to update project name and team id
    """

    def __init__(self, project_name, owning_team):
        """

        Args:
            project_name (str):
            owning_team (int): team_id
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

    def __str__(self):
        return "CxUpdateProjectNameTeamIdRequest(project_name={}, owning_team={})".format(
            self.project_name, self.owning_team
        )
