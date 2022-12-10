class RoleRepresentation:
    def __init__(self, attributes, client_role, composite, composites, container_id, description,
                 role_representation_id, name):
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

    def get_post_data(self):
        import json
        return json.dumps({
            "attributes": self.attributes,
            "clientRole": self.clientRole,
            "composite": self.composite,
            "composites": self.composites,
            "containerId": self.containerId,
            "description": self.description,
            "id": self.id,
            "name": self.name,
        })


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
