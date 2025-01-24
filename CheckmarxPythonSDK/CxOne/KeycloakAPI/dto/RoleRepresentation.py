class RoleRepresentation:
    def __init__(self, client_role, composite, container_id,
                 role_representation_id, name,
                 attributes=None, composites=None, description=None):
        self.attributes = attributes
        self.clientRole = client_role
        self.composite = composite
        self.composites = composites
        self.containerId = container_id
        self.description = description
        self.id = role_representation_id
        self.name = name

    def __str__(self):
        return f"RoleRepresentation(" \
               f"attributes={self.attributes} " \
               f"clientRole={self.clientRole} " \
               f"composite={self.composite} " \
               f"composites={self.composites} " \
               f"containerId={self.containerId} " \
               f"description={self.description} " \
               f"id={self.id} " \
               f"name={self.name} " \
               f")"

    def to_dict(self):
        data = {
            "clientRole": self.clientRole,
            "composite": self.composite,
            "containerId": self.containerId,
            "id": self.id,
            "name": self.name,
        }
        if self.attributes:
            data.update({"attributes": self.attributes})
        if self.description:
            data.update({"description": self.description})
        if self.composites:
            data.update({"composites": self.composites})
        return data


def construct_role_representation(item):
    return RoleRepresentation(
        attributes=item.get("attributes"),
        client_role=item.get("clientRole"),
        composite=item.get("composite"),
        composites=item.get("composites"),
        container_id=item.get("containerId"),
        description=item.get("description"),
        role_representation_id=item.get("id"),
        name=item.get("name"),
    )
