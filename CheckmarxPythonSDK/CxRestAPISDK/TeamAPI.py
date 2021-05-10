# encoding: utf-8
import requests


from ..compat import OK, BAD_REQUEST, NOT_FOUND, UNAUTHORIZED, CREATED
from ..config import config

from . import authHeaders
from .exceptions.CxError import BadRequestError, NotFoundError, CxError
from .team.dto import CxTeam, CxCreateTeamRequest


class TeamAPI(object):
    """
    the team api
    """

    def __init__(self):
        self.retry = 0

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
        teams_url = config.get("base_url") + "/cxrestapi/auth/teams"

        r = requests.get(
            url=teams_url,
            headers=authHeaders.auth_headers,
            verify=config.get("verify")
        )
        if r.status_code == OK:
            a_list = r.json()
            teams = [
                CxTeam(
                    item.get("id"), item.get("name"), item.get("fullName"), item.get("parentId")
                ) for item in a_list
            ]
        elif r.status_code == BAD_REQUEST:
            raise BadRequestError(r.text)
        elif r.status_code == NOT_FOUND:
            raise NotFoundError()
        elif (r.status_code == UNAUTHORIZED) and (self.retry < config.get("max_try")):
            authHeaders.update_auth_headers()
            self.retry += 1
            teams = self.get_all_teams()
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

    def create_team(self, team_name, parent_id):
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

        teams_url = config.get("base_url") + "/cxrestapi/auth/teams"

        req_data = CxCreateTeamRequest(team_name, parent_id).get_post_data()
        r = requests.post(
            url=teams_url,
            data=req_data,
            headers=authHeaders.auth_headers,
            verify=config.get("verify")
        )
        if r.status_code == CREATED:
            # The create team API returns the location of the new team
            # in the Location header. E.g.: /cxrestapi/auth/Teams/8
            location = r.headers['Location']
            parts = location.split('/')
            team_id = int(parts[-1])
            return team_id
        elif r.status_code == BAD_REQUEST:
            raise BadRequestError(r.text)
        elif (r.status_code == UNAUTHORIZED) and (self.retry < config.get("max_try")):
            authHeaders.update_auth_headers()
            self.retry += 1
            self.create_team(team_name, parent_id)
        else:
            raise CxError(r.text, r.status_code)

        self.retry = 0
