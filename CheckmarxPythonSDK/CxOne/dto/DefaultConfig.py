from dataclasses import dataclass


@dataclass
class DefaultConfig:
    """

    Attributes:
        name (str): Name of the default config
        description (str): Description of the default config
        url (str): Url for the default config file
    """
    name: str
    description: str
    url: str

    def to_dict(self):
        return {
            "name": self.name,
            "description": self.description,
            "url": self.url,
        }


def construct_default_config(item):
    return DefaultConfig(
        name=item.get("name"),
        description=item.get("description"),
        url=item.get("url"),
    )
