# encoding: utf-8
import json
from CheckmarxPythonSDK.utilities.compat import OK, CREATED
from .team.dto import CxTeam
from .httpRequests import get_request, post_request, get_headers


class TeamAPI(object):
    """
    the team api
    """

    @staticmethod
    def get_all_teams():
        """
        REST API: get all teams

        Returns:
            :obj:`list` of :obj:`CxTeam`

        Raises:
            BadRequestError
            notFoundError
            CxError
        """
        result = []
        relative_url = "/cxrestapi/auth/teams"
        response = get_request(relative_url=relative_url, headers=get_headers())
        if response.status_code == OK:
            result = [
                CxTeam(
                    item.get("id"), item.get("name"), item.get("fullName"), item.get("parentId")
                ) for item in response.json()
            ]
        return result

    @staticmethod
    def get_team_id_by_team_full_name(team_full_name):
        """
        utility provided by SDK: get team id by team full name

        Args:
            team_full_name (str): the team full name, for example "/CxServer/SP/Company/Users".
            note that, team name is not unique.

        Returns:
            int: the team id for the team full name
        """
        all_teams = TeamAPI.get_all_teams()

        # construct a dict of {team_full_name: team_id}
        team_full_name_id_dict = {item.full_name: item.team_id for item in all_teams}

        if team_full_name.startswith("CxServer"):
            team_full_name = "/" + team_full_name.replace("\\", "/")

        team_id = team_full_name_id_dict.get(team_full_name.replace("\\", "/"))

        return team_id

    @staticmethod
    def get_team_full_name_by_team_id(team_id):
        """
        utility provided by SDK: get team full name by team id

        Args:
            team_id (int, str):

        Returns:
            str: team full name, "/CxServer/SP/Company/Users"

        """
        all_teams = TeamAPI.get_all_teams()

        # construct a dict of team_id: team_full_name
        team_id_team_full_name_dict = {item.team_id: item.full_name for item in all_teams}

        return team_id_team_full_name_dict.get(team_id)

    @staticmethod
    def create_team(team_name, parent_id):
        """
        REST API: create team

        Args:
            team_name (str): Specifies the name of the team
            parent_id (int): specifies the identifier of the parent team

        Returns:
            The id of the new team

        Raises:
            BadRequestError
            CxError
        """
        result = None
        relative_url = "/cxrestapi/auth/teams"
        post_data = json.dumps(
            {
                "name": team_name,
                "parentId": parent_id
            }
        )
        response = post_request(relative_url=relative_url, data=post_data, headers=get_headers())
        if response.status_code == CREATED:
            # The create team API returns the location of the new team
            # in the Location header. E.g.: /cxrestapi/auth/Teams/8
            location = response.headers['Location']
            parts = location.split('/')
            result = int(parts[-1])
        return result
