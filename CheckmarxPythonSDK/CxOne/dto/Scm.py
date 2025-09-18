from dataclasses import dataclass


@dataclass
class Scm:
    """

    Attributes:
        token (str): The token for authentication with your SCM
        type (str): The type of SCM that you are importing from
        self_hosted_scm_url (str): The URL of your self-hosted environment. Note: This should be the exact URL that
            you configured for your code repository in Checkmarx One.
    """

    token: str
    type: str = "github"
    self_hosted_scm_url: str = None

    def to_dict(self):
        return {
            "type": self.type,
            "token": self.token
        }


def construct_scm(item):
    return Scm(
        type=item.get("type"),
        token=item.get("token"),
        self_hosted_scm_url=item.get("selfHostedScmUrl")
    )
