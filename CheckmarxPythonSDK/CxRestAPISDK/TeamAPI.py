# encoding: utf-8
import requests

from ...compat import OK, BAD_REQUEST, NOT_FOUND, UNAUTHORIZED

from ..auth import AuthenticationAPI
from ...config import config
from ..exceptions.CxError import BadRequestError, NotFoundError, CxError
from .dto import CxTeam


class TeamAPI(object):
    """
    the team api
    """

    teams = []

    def __init__(self):
        self.retry = 0
        self.get_all_teams()
        self.get_team_id_by_team_full_name()

    def get_all_teams(self):
        """
        REST API: get all teams

        Returns:
            :obj:`list` of :obj:`CxTeam`

        Raises:
            BadRequestError
            notFoundError
            CxError
        """
        teams = []

        teams_url = config.get("base_url") + "/cxrestapi/auth/teams"

        r = requests.get(
            url=teams_url,
            headers=AuthenticationAPI.AuthenticationAPI.auth_headers,
            verify=config.get("verify")
        )
        if r.status_code == OK:
            a_list = r.json()
            teams = [
                CxTeam.CxTeam(
                    item.get("id"), item.get("name"), item.get("fullName"), item.get("parentId")
                ) for item in a_list
            ]
            TeamAPI.teams = teams
        elif r.status_code == BAD_REQUEST:
            raise BadRequestError(r.text)
        elif r.status_code == NOT_FOUND:
            raise NotFoundError()
        elif (r.status_code == UNAUTHORIZED) and (self.retry < config.get("max_try")):
            AuthenticationAPI.AuthenticationAPI.reset_auth_headers()
            self.retry += 1
            self.get_all_teams()
        else:
            raise CxError(r.text, r.status_code)

        self.retry = 0

        return teams

    def get_team_id_by_team_full_name(self, team_full_name=config.get("team_full_name")):
        """
        utility provided by SDK: get team id by team full name

        Args:
            team_full_name (str): the team full name, for example "/CxServer/SP/Company/Users".
            note that, team name is not unique.

        Returns:
            int: the team id for the team full name
        """
        all_teams = self.get_all_teams()

        # construct a dict of {team_full_name: team_id}
        team_full_name_id_dict = {item.full_name: item.team_id for item in all_teams}

        team_id = team_full_name_id_dict.get(team_full_name.replace("\\", "/"))

        return team_id

    def get_team_full_name_by_team_id(self, team_id):
        """
        utility provided by SDK: get team full name by team id

        Args:
            team_id (int, str):

        Returns:
            str: team full name, "/CxServer/SP/Company/Users"

        """
        all_teams = self.get_all_teams()

        # construct a dict of team_id: team_full_name
        team_id_team_full_name_dict = {item.team_id: item.full_name for item in all_teams}

        return team_id_team_full_name_dict.get(team_id)
