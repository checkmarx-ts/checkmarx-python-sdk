# encoding: utf-8
import json
from .BranchInput import BranchInput
from ..utilities import type_check, list_member_type_check


class RepoScmImportInput(object):
    def __init__(self, isRepoAdmin=None, id=None, name=None, origin=None, url=None, branches=None, kicsScannerEnabled=True,
                 sastIncrementalScan=False, sastScannerEnabled=True, apiSecScannerEnabled=True, scaScannerEnabled=True,
                 webhookEnabled=True, prDecorationEnabled=True, sshRepoUrl=None, sshState="SKIPPED", repoId=None):
        """

        Args:
            isRepoAdmin (bool): The name that you would like to assign to the new Project. The Project name must be unique.
            id (str): id of the repo
            name (str): name of the repo
            origin(str): Github | Bitbucket | Gitlab | ADO
            url (str): git url of repo
            branches (BranchInput) : branch details for protected branch
            kicksScannerEnabled (bool): enable kicks scans
            sastIncrementalScan (bool): enable incremental scan
            sastScannerEnabled (bool): enable sast scans
            apiSecScannerEnabled (bool): enable api security scans
            scaScannerEnabled (bool): enable sca scans
            webhookEnabled (bool): enable webhooks
            prDecorationEnabled (bool): enable PR decoration
            sshRepoUrl (str): ssh url for the repo
            sshState (str): SKIPPED
            repoId (str) : N/A
        """
        type_check(isRepoAdmin, bool)
        type_check(id, str)
        type_check(name, str)
        type_check(origin, str)
        type_check(url, str)
        type_check(branches, BranchInput)
        type_check(kicsScannerEnabled, bool)
        type_check(sastIncrementalScan, bool)
        type_check(sastScannerEnabled, bool)
        type_check(apiSecScannerEnabled, bool)
        type_check(scaScannerEnabled, bool)
        type_check(webhookEnabled, bool)
        type_check(prDecorationEnabled, bool)
        type_check(sshRepoUrl, str)
        type_check(sshState, str)

        self.isRepoAdmin = isRepoAdmin
        self.id = id
        self.name = name
        self.origin = origin
        self.url = url
        self.branches = branches
        self.kicsScannerEnabled = kicsScannerEnabled
        self.sastIncrementalScan = sastIncrementalScan
        self.sastScannerEnabled = sastScannerEnabled
        self.apiSecScannerEnabled = apiSecScannerEnabled
        self.scaScannerEnabled = scaScannerEnabled
        self.webhookEnabled = webhookEnabled
        self.prDecorationEnabled = prDecorationEnabled
        self.sshRepoUrl = sshRepoUrl
        self.sshState = sshState
        self.repoId = repoId

    def __str__(self):
        return """RepoScmImportInput(isRepoAdmin={}, id={}, name={}, origin={}, branches={},
        kicsScannerEnabled={}, sastIncrementalScan={}, sastScannerEnabled={}, apiSecScannerEnabled={},
        scaScannerEnabled={}, webhookEnabled={}, prDecorationEnabled={}, sshRepoUrl={}, sshState={}, repoId={} )""".format(
            self.name,
            self.id,
            self.name,
            self.origin,
            self.branches,
            self.kicsScannerEnabled,
            self.sastIncrementalScan,
            self.sastScannerEnabled,
            self.apiSecScannerEnabled,
            self.scaScannerEnabled,
            self.webhookEnabled,
            self.prDecorationEnabled,
            self.sshRepoUrl,
            self.sshState,
            self.repoId
        )

    def get_post_data(self):
        data = {}
        reposFromRequest = []
        branches = []
        branch = {}
        formData = {}
        branch.update({"name":self.branches.name})
        branch.update({"isDefaultBranch":self.branches.isDefaultBranch})
        branches.append(branch)
        if self.name:
            formData.update({"id": self.id})
            formData.update({"name": self.name})
            formData.update({"url": self.url})
            formData.update({"origin": self.origin})
            formData.update({"branches": branches})
            formData.update({"kicsScannerEnabled": self.kicsScannerEnabled})
            formData.update({"sastIncrementalScan": self.sastIncrementalScan})
            formData.update({"sastScannerEnabled": self.sastScannerEnabled})
            formData.update({"apiSecScannerEnabled": self.apiSecScannerEnabled})
            formData.update({"scaScannerEnabled": self.scaScannerEnabled})
            formData.update({"webhookEnabled": self.webhookEnabled})
            formData.update({"prDecorationEnabled": self.prDecorationEnabled})
            formData.update({"sshRepoUrl": ""})
            formData.update({"sshState": "SKIPPED"})

            reposFromRequest.append(formData)
            data["reposFromRequest"]=reposFromRequest
            data.update({"orgSshKey": ""})
            data.update({"orgSshState": "SKIPPED"})
        return json.dumps(data)
