from dataclasses import dataclass


@dataclass
class DefaultConfig:
    """

    Attributes:
        name (str): Name of the default config
        description (str): Description of the default config
        url (str): Url for the default config file
    """

    name: str = None
    description: str = None
    url: str = None
