# encoding: utf-8

"""
    tests.test_team

    :copyright Checkmarx
    :license MIT

"""

from CheckmarxPythonSDK.CxRestAPISDK import TeamAPI


def test_team():
    team_api = TeamAPI()
    teams = team_api.get_all_teams()
    assert len(teams) > 0
    team_id = team_api.get_team_id_by_team_full_name("/CxServer")
    assert team_id is not None

def test_get_team_id_by_team_full_name():
    team_api = TeamAPI()
    team_id = team_api.get_team_id_by_team_full_name("CxServer\\SP\\Company")
    assert team_id is not None
