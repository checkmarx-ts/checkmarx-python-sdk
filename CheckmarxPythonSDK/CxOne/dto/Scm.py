class Scm(object):

    def __init__(self,
                 token: str,
                 scm_type: str = "github",
                 self_hosted_scm_url: str = None
                 ):
        """

        Args:
            token (str): The token for authentication with your SCM
            scm_type (str): The type of SCM that you are importing from
            self_hosted_scm_url (str): The URL of your self-hosted environment. Note: This should be the exact URL that
                you configured for your code repository in Checkmarx One.
        """
        self.type = scm_type
        self.token = token
        self.selfHostedScmUrl = self_hosted_scm_url

    def __str__(self):
        return f"Scm(type={self.type}, token={self.token}, selfHostedScmUrl={self.selfHostedScmUrl}"

    def to_dict(self):
        return {
            "type": self.type,
            "token": self.token
        }
