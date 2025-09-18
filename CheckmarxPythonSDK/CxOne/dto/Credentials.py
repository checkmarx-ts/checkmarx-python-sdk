from dataclasses import dataclass


@dataclass
class Credentials:
    """

    Attributes:
        username (str): The username required for accessing the Git repository.
        type (str): The type of credentials used for accessing the Git repository.
                 apiKey, password, ssh, JWT
        value (str): The credentials used for accessing the Git repository.
    """
    username: str
    type: str
    value: str

    def to_dict(self):
        return {
            "username": self.username,
            "type": self.type,
            "value": self.value,
        }
