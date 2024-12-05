import os
from CheckmarxPythonSDK.CxOne import (
    import_code_repository,
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
    scm_import_input = SCMImportInput(
        scm=Scm(token=os.getenv("GITHUB_TOKEN")),
        organization=ScmOrganization(org_identity=os.getenv("GITHUB_ORG"), monitor_for_new_projects=True),
        default_project_settings=ProjectSettings(
            web_hook_enabled=True,
            decorate_pull_requests=True,
            is_private_package=True,
            scanners=[
                Scanner(scanner_type="sast", auto_pr_enabled=True,
                        incremental=True),
                Scanner(scanner_type="sca", auto_pr_enabled=True, incremental=True)
            ],
            tags={"key": "value"},
            groups=["AlphaTeam"]
        ),
        scan_projects_after_import=True,
        projects=[
            ScmProject(
                scm_repository_url="https://github.com/HappyY19/cxclipy",
                protected_branches=["main"],
                branch_to_scan_upon_creation="main"
            )
        ]
    )
    response = import_code_repository(scm_import_input)
    assert response is not None
