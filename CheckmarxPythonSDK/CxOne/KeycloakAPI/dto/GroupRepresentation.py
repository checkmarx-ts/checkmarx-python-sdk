class GroupRepresentation:
    def __init__(self, access, attributes, client_roles, group_representation_id, name, path, realm_roles, sub_groups):
        self.access = access
        self.attributes = attributes
        self.clientRoles = client_roles
        self.id = group_representation_id
        self.name = name
        self.path = path
        self.realmRoles = realm_roles
        self.subGroups = sub_groups

    def __str__(self):
        return f"GroupRepresentation(" \
               f"access={self.access} " \
               f"attributes={self.attributes} " \
               f"clientRoles={self.clientRoles} " \
               f"id={self.id} " \
               f"name={self.name} " \
               f"path={self.path} " \
               f"realmRoles={self.realmRoles} " \
               f"subGroups={self.subGroups} " \
               f")"

    def to_dict(self):
        return {
            "access": self.access,
            "attributes": self.attributes,
            "clientRoles": self.clientRoles,
            "id": self.id,
            "name": self.name,
            "path": self.path,
            "realmRoles": self.realmRoles,
            "subGroups": self.subGroups,
        }


def construct_group_representation(item):
    return GroupRepresentation(
        access=item.get("access"),
        attributes=item.get("attributes"),
        client_roles=item.get("clientRoles"),
        group_representation_id=item.get("id"),
        name=item.get("name"),
        path=item.get("path"),
        realm_roles=item.get("realmRoles"),
        sub_groups=item.get("subGroups"),
    )
