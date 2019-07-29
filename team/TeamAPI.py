# encoding: utf-8
import http

import requests

from auth import AuthenticationAPI
from config import CxConfig

from team.dto import CxTeam


class TeamAPI(object):
    """
    the team api
    """
    teams = []
    teams_url = CxConfig.CxConfig.config.url + "/auth/teams"

    def __init__(self):
        self.get_all_teams()
        self.retry = 0

    def get_all_teams(self):
        """
        REST API: get all teams
        :return:
        list of CxTeam
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
            raise Exception("Bad Request")
        elif (r.status_code == http.HTTPStatus.UNAUTHORIZED) and (self.retry < 3):
            AuthenticationAPI.AuthenticationAPI.reset_auth_headers()
            self.retry += 1
            self.get_all_teams()
        else:
            raise Exception("Network Error")
        return teams

    def get_team_id_by_full_name(self, team_full_name=CxConfig.CxConfig.config.team):
        """
        utility provided by SDK: get team id by team full name
        :param team_full_name: str
            the team full name, for example "/CxServer/SP/Company/Users". note that, team name is not unique.
        :return:
        int
            the team id for the team full name
        """
        all_teams = self.get_all_teams()
        # construct a dict of team_full_name: team_id
        team_full_name_id_dict = {item.full_name: item.team_id for item in all_teams}
        return team_full_name_id_dict.get(team_full_name)
