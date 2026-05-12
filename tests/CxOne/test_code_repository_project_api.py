import os
import pytest
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
    github_token = os.getenv("GITHUB_TOKEN")
    if not github_token:
        pytest.skip("GITHUB_TOKEN environment variable not set")
    github_org = "cx-happy-yang"
    scm_import_input = SCMImportInput(
        scm=Scm(token=github_token),
        organization=ScmOrganization(orgIdentity=github_org, monitorForNewProjects=False),
        defaultProjectSettings=ProjectSettings(
            webhookEnabled=False,
            decoratePullRequests=False,
            scanners=[
                Scanner(type="sast", incrementalScan=False),
                Scanner(type="sca", enableAutoPullRequests=False),
                Scanner(type="apisec"),
                Scanner(type="kics"),
            ]
        ),
        scanProjectsAfterImport=False,
        projects=[
            ScmProject(
                scmRepositoryUrl=f"https://github.com/{github_org}/cxclipy",
                protectedBranches=["main"],
                branchToScanUponCreation="main"
            ),
            ScmProject(
                scmRepositoryUrl=f"https://github.com/{github_org}/JavaVulnerableLab",
                protectedBranches=["master"],
                branchToScanUponCreation="master"
            )
        ]
    )
    import_response = import_code_repository(scm_import_input)
    assert import_response is not None

    process_id = import_response.get("processId")
    status_response = retrieve_import_status(process_id=process_id)
    assert status_response is not None
