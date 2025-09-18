from CheckmarxPythonSDK.CxOne import (
    check_if_scan_has_source_code_available,
    get_project_id_by_name,
    get_the_list_of_branches_inside_a_git_repository,
)

commit_id = "82a3db68dda8d213aa47abe99f7f76455c3f677b"
new_project_name = "happy-test-2022-04-20"


def test_check_if_scan_has_source_code_available():
    result = check_if_scan_has_source_code_available("edcba8aa-2498-4d80-b4e5-4d83ff85930b")
    assert result is not None


def test_get_the_list_of_branches_inside_a_git_repository():
    project_id = get_project_id_by_name(name=new_project_name)
    repo_url = "https://github.com/CSPF-Founder/JavaVulnerableLab.git"
    token = None
    branches = get_the_list_of_branches_inside_a_git_repository(project_id=project_id, repo_url=repo_url, token=token)
    assert branches is not None
