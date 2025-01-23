class DefaultConfig:
    def __init__(self, name, description, url):
        """

        Args:
            name (str): Name of the default config
            description (str): Description of the default config
            url (str): Url for the default config file
        """
        self.name = name
        self.description = description
        self.url = url

    def __str__(self):
        return f"DefaultConfig(" \
               f"name={self.name} " \
               f"description={self.description} " \
               f"url={self.url} " \
               f")"

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
