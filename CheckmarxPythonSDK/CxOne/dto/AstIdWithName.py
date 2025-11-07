from dataclasses import dataclass


@dataclass
class AstIdWithName:
    """

     Attributes:
         id (str):
         name (str):
         brief_name (str):
         parent_id (str)
     """
    id: str
    name: str
    brief_name: str
    parent_id: str


def construct_ast_id_with_name(item):
    return AstIdWithName(
        id=item.get("id"),
        name=item.get("name"),
        brief_name=item.get("briefName"),
        parent_id=item.get("parentId"),
    )
