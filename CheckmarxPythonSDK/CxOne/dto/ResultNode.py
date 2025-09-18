from dataclasses import dataclass


@dataclass
class ResultNode:
    """
    Attributes:
        column (int): Column position of the node
        file_name (str): Full file name of the containing source file
        full_name (str): FQN of the node
        length (int): Length of the node
        line (int): Line position of the node
        method_line (int): Line position of the containing method,
        method (str):
        name (str): node name
        dom_type (str): node DomType
        node_hash (str):
    """
    column: int
    file_name: str
    full_name: str
    length: int
    line: int
    method_line: int
    method: str
    name: str
    dom_type: str
    node_hash: str = None


def construct_result_node(item):
    return ResultNode(
        column=item.get("column"),
        file_name=item.get('fileName'),
        full_name=item.get('fullName'),
        length=item.get('length'),
        line=item.get('line'),
        method_line=item.get('methodLine'),
        method=item.get("method"),
        name=item.get('name'),
        dom_type=item.get('domType'),
        node_hash=item.get("nodeHash"),
    )
