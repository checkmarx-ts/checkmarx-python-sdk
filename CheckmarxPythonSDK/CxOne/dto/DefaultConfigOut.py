class DefaultConfigOut:
    def __init__(self, default_config_out_id, name, description, url, is_tenant_default, associated_projects):
        """

        Args:
            default_config_out_id (str):  Id of the default config
            name (str): Name of the default config
            description (str): Description of the default config
            url (str): Url for the default config file
            is_tenant_default (bool): Boolean when in use by tenant
            associated_projects (int): The number of associated projects
        """
        self.id = default_config_out_id
        self.name = name
        self.description = description
        self.url = url
        self.isTenantDefault = is_tenant_default
        self.associatedProjects = associated_projects

    def __str__(self):
        return f"DefaultConfigOut(" \
               f"id={self.id} " \
               f"name={self.name} " \
               f"description={self.description} " \
               f"url={self.url} " \
               f"isTenantDefault={self.isTenantDefault} " \
               f"associatedProjects={self.associatedProjects} " \
               f")"

    def to_dict(self):
        return {
            "id": self.id,
            "name": self.name,
            "description": self.description,
            "url": self.url,
            "isTenantDefault": self.isTenantDefault,
            "associatedProjects": self.associatedProjects,
        }


def construct_default_config_out(item):
    return DefaultConfigOut(
        default_config_out_id=item.get("id"),
        name=item.get("name"),
        description=item.get("description"),
        url=item.get("url"),
        is_tenant_default=item.get("isTenantDefault"),
        associated_projects=item.get("associatedProjects"),
    )
