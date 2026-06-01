from dataclasses import dataclass


@dataclass
class DastUserCredentials:
    username: str = None
    password: str = None

    @classmethod
    def from_dict(cls, item: dict) -> "DastUserCredentials":
        return cls(
            username=item.get("Username"),
            password=item.get("Password"),
        )
