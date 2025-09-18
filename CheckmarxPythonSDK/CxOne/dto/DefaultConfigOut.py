from dataclasses import dataclass


@dataclass
class DefaultConfigOut:
    """

    Attributes:
        id (str):  Id of the default config
        name (str): Name of the default config
        description (str): Description of the default config
        url (str): Url for the default config file
        is_tenant_default (bool): Boolean when in use by tenant
        associated_projects (int): The number of associated projects
    """
    id: str
    name: str
    description: str
    url: str
    is_tenant_default: bool
    associated_projects: int

    def to_dict(self):
        return {
            "id": self.id,
            "name": self.name,
            "description": self.description,
            "url": self.url,
            "isTenantDefault": self.is_tenant_default,
            "associatedProjects": self.associated_projects,
        }


def construct_default_config_out(item):
    return DefaultConfigOut(
        id=item.get("id"),
        name=item.get("name"),
        description=item.get("description"),
        url=item.get("url"),
        is_tenant_default=item.get("isTenantDefault"),
        associated_projects=item.get("associatedProjects"),
    )
