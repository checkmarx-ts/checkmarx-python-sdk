# encoding: utf-8
import http

import requests

from pathlib import Path

from ..auth import AuthenticationAPI
from ..config import CxConfig
from ..exceptions.CxError import BadRequestError, NotFoundError, UnknownHttpStatusError
from .dto import CxTeam


class TeamAPI(object):
    """
    the team api
    """
    max_try = CxConfig.CxConfig.config.max_try
    teams = []
    teams_url = CxConfig.CxConfig.config.url + "/auth/teams"
    default_team_id = None

    def __init__(self):
        self.get_all_teams()
        self.retry = 0
        self.get_team_id_by_team_full_name()

    def get_all_teams(self):
        """
        REST API: get all teams

        Returns:
            :obj:`list` of :obj:`CxTeam`

        Raises:
            BadRequestError
            notFoundError
            UnknownHttpStatusError
        """
        teams = []
        r = requests.get(TeamAPI.teams_url, headers=AuthenticationAPI.AuthenticationAPI.auth_headers)
        if r.status_code == http.HTTPStatus.OK:
            a_list = r.json()
            teams = [
                CxTeam.CxTeam(
                    item.get("id"), item.get("name"), item.get("fullName"), item.get("parentId")
                ) for item in a_list
            ]
            TeamAPI.teams = teams
        elif r.status_code == http.HTTPStatus.BAD_REQUEST:
            raise BadRequestError(r.text)
        elif r.status_code == http.HTTPStatus.NOT_FOUND:
            raise NotFoundError()
        elif (r.status_code == http.HTTPStatus.UNAUTHORIZED) and (self.retry < self.max_try):
            AuthenticationAPI.AuthenticationAPI.reset_auth_headers()
            self.retry += 1
            self.get_all_teams()
        else:
            raise UnknownHttpStatusError()

        self.retry = 0

        return teams

    def get_team_id_by_team_full_name(self, team_full_name=CxConfig.CxConfig.config.team_full_name):
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

        team_id = team_full_name_id_dict.get(Path(team_full_name.replace("\\", "/")))
        TeamAPI.default_team_id = team_id

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
