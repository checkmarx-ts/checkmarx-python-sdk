# encoding: utf-8

"""
    tests.test_team
"""

from CheckmarxPythonSDK.CxRestAPISDK import TeamAPI


def test_team():
    team_api = TeamAPI()
    teams = team_api.get_all_teams()
    assert len(teams) > 0
    team_id = team_api.get_team_id_by_team_full_name("/CxServer")
    assert team_id is not None
    team_full_name = team_api.get_team_full_name_by_team_id(1)
    assert team_full_name == "/CxServer"
    team_id = team_api.get_team_id_by_team_full_name("/CxServer/Dagger Team")
    if not team_id:
        new_team_id = team_api.create_team("Dagger Team", 1)
        assert new_team_id > 1
