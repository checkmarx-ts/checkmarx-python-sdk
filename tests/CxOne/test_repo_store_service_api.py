from CheckmarxPythonSDK.CxOne import (
    check_if_scan_has_source_code_available,
    get_project_id_by_name,
    get_commit_content,
    get_folder_content,
    get_code,
    get_project_tree_structure,
    get_the_list_of_branches_inside_a_git_repository,
)

commit_id = "82a3db68dda8d213aa47abe99f7f76455c3f677b"
new_project_name = "happy-test-2022-04-20"


def test_check_if_scan_has_source_code_available():
    result = check_if_scan_has_source_code_available("edcba8aa-2498-4d80-b4e5-4d83ff85930b")
    assert result is not None


def test_get_commit_content():
    commit_content = get_commit_content(commit_id=commit_id)
    assert commit_content is not None
    # 'HttpStatusCode: 400', 'ErrorMessage: {"message":"CommitID must be UUID","code":1002}{"message":"Commit not found","code":1001}


def test_get_folder_content():
    folder = ""
    folder_content = get_folder_content(commit_id=commit_id, folder=folder)
    assert folder_content is not None


def test_get_code():
    file_name = ""
    code = get_code(commit_id=commit_id, file_name=file_name)
    assert code is not None


def test_get_project_tree_structure():
    tree_structure = get_project_tree_structure(commit_id=commit_id)
    assert tree_structure is not None


def test_get_the_list_of_branches_inside_a_git_repository():
    project_id = get_project_id_by_name(name=new_project_name)
    repo_url = "https://github.com/CSPF-Founder/JavaVulnerableLab.git"
    token = None
    branches = get_the_list_of_branches_inside_a_git_repository(project_id=project_id, repo_url=repo_url, token=token)
    assert branches is not None
