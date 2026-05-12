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
