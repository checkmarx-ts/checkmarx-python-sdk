"""
    tests.test_projects_api

    :copyright Checkmarx
    :license GPL-3

"""

from CheckmarxPythonSDK.CxRestAPISDK import TeamAPI


def test_team():
    team_api = TeamAPI()
    teams = team_api.get_all_teams()
    assert len(teams) > 0
    root_team_id = team_api.get_team_id_by_team_full_name("/CxServer")
    assert root_team_id is not None
    team_full_name = team_api.get_team_full_name_by_team_id(root_team_id)
    assert team_full_name == "/CxServer"
    dagger_team_id = team_api.get_team_id_by_team_full_name("/CxServer/Dagger Team")
    if not dagger_team_id:
        try:
            new_team_id = team_api.create_team("Dagger Team", root_team_id)
            assert new_team_id > 1
        except ValueError:
            pass
