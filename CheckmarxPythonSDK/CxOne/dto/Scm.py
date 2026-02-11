from dataclasses import dataclass


@dataclass
class Scm:
    """

    Attributes:
        token (str): The token for authentication with your SCM, Allowed values:github, githubApp
        type (str): The token for authentication with your SCM. Note: For integrations via 
                    GitHub Apps, this field is not relevant.
        self_hosted_scm_url (str): If you are using our Self-Hosted flow, submit the URL of your self-hosted environment.
                                   Note: The initial step of creating a code repository instance (by submitting an 
                                   Instance Name, URL, and authentication credentials) must be done via the UI. 
                                   Then you must submit here the exact URL that you configured in the UI.
            
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
