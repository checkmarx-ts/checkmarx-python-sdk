from dataclasses import dataclass
from .Scm import Scm
from .ScmOrganization import ScmOrganization
from .ProjectSettings import ProjectSettings
from .ScmProject import ScmProject
from typing import List


@dataclass
class SCMImportInput:
    """

    Attributes:
        scm (Scm):
        organization (ScmOrganization):
        defaultProjectSettings (ProjectSettings): By default, these settings will be applied to each
            project created by this process. You can configure different settings for specific projects, which will
            override these settings.
        scanProjectsAfterImport (bool): If true an initial scan will be run when the import process is completed
        projects (list of ScmProject): Specify the repos that you would like to import.
            Each repo needs to be submitted explicitly.
            Note: You can specify project settings for each specific project. These settings override the
            defaultProjectSettings
    """

    scm: Scm
    organization: ScmOrganization
    defaultProjectSettings: ProjectSettings
    scanProjectsAfterImport: bool
    projects: List[ScmProject]
