# encoding: utf-8
class Credentials(object):
    def __init__(self, username, credential_type, value):
        """

        Args:
            username (str): The user name required for accessing the Git repository.
            credential_type (str): The type of credentials used for accessing the Git repository.
                     apiKey, password, ssh, JWT
            value (str): The credentials used for accessing the Git repository.
        """
        self.username = username
        if credential_type not in ("apiKey", "password", "ssh", "JWT"):
            raise ValueError('Git Credential type must be one of ["apiKey", "password", "ssh", "JWT"]')
        self.type = credential_type
        self.value = value

    def __str__(self):
        return """GitCredential(username={}, type={}, value={})""".format(
            self.username, self.type, self.value
        )

    def as_dict(self):
        return {
            "username": self.username,
            "type": self.type,
            "value": self.value,
        }
