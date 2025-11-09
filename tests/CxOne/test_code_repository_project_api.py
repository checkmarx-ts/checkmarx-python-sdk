import os
from CheckmarxPythonSDK.CxOne import (
    import_code_repository,
    retrieve_import_status,
)

from CheckmarxPythonSDK.CxOne.dto import (
    SCMImportInput,
    Scm,
    ScmOrganization,
    ProjectSettings,
    ScmProject,
    Scanner,
)


def test_import_code_repository():
    github_org = "cx-happy-yang"
    scm_import_input = SCMImportInput(
        scm=Scm(token=os.getenv("GITHUB_TOKEN")),
        organization=ScmOrganization(org_identity=github_org, monitor_for_new_projects=False),
        default_project_settings=ProjectSettings(
            web_hook_enabled=False,
            decorate_pull_requests=False,
            scanners=[
                Scanner(type="sast", incremental_scan=False),
                Scanner(type="sca", enable_auto_pull_requests=False),
                Scanner(type="apisec"),
                Scanner(type="kics"),
            ]
        ),
        scan_projects_after_import=False,
        projects=[
            ScmProject(
                scm_repository_url=f"https://github.com/{github_org}/cxclipy",
                protected_branches=["main"],
                branch_to_scan_upon_creation="main"
            ),
            ScmProject(
                scm_repository_url=f"https://github.com/{github_org}/JavaVulnerableLab",
                protected_branches=["master"],
                branch_to_scan_upon_creation="master"
            )
        ]
    )
    import_response = import_code_repository(scm_import_input)
    assert import_response is not None

    process_id = import_response.get("processId")
    status_response = retrieve_import_status(process_id=process_id)
    assert status_response is not None
