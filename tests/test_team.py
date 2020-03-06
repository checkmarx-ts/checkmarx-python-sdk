# encoding: utf-8

"""
    tests.test_team

    :copyright Checkmarx
    :license MIT

"""

from CheckmarxPythonSDK.CxRestAPISDK.team import TeamAPI


def test_team():
    teams = TeamAPI.TeamAPI()
    assert teams.teams is not None
    assert len(teams.teams) > 0
    team_id = teams.get_team_id_by_team_full_name("/CxServer")
    assert team_id is not None

