from dataclasses import dataclass
from .dto import Composites


@dataclass
class RoleRepresentation:
    id: str
    name: str
    description: str
    scope_param_required: bool
    composite: bool
    composites: Composites
    client_role: bool
    container_id: str
    attributes: dict

    def to_dict(self):
        data = {
            "clientRole": self.client_role,
            "composite": self.composite,
            "containerId": self.container_id,
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
        id=item.get("id"),
        name=item.get("name"),
        description=item.get("description"),
        scope_param_required=item.get("scopeParamRequired"),
        composite=item.get("composite"),
        composites=item.get("composites"),
        client_role=item.get("clientRole"),
        container_id=item.get("containerId"),
        attributes=item.get("attributes"),
    )
