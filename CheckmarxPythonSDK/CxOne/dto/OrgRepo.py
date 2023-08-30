class OrgRepo(object):
    def __init__(self, id, name, url, defaultBranch, fullName, isRepoAdmin, privatePackage, sshRepoUrl):
        """

        Args:
            id (str): Severity enum of a result. Enum: [ HIGH, MEDIUM, LOW, INFO ]
            name (str):
            isUser (str):
        """
        self.id = id
        self.name = name
        self.url = url
        self.defaultBranch = defaultBranch
        self.fullName = fullName
        self.isRepoAdmin = isRepoAdmin
        self.privatePackage = privatePackage
        self.sshRepoUrl = sshRepoUrl

    def __str__(self):
        return """scmOrg(id={}, name={})""".format(
            self.id, self.name
        )

    def as_dict(self):
        data = {}
        if self.id:
            data.update({"id": self.id})
        if self.name:
            data.update({"tags": self.name})
        return data