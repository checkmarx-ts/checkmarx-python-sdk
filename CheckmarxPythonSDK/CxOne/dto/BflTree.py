from dataclasses import dataclass
from .ResultNode import ResultNode, construct_result_node
from .SastResult import SastResult, construct_sast_result
from typing import List


@dataclass
class BflTree:
    """
    Attributes:
        id (str): tree ID in the forest
        bfl (ResultNode): Best Fix Location node of the tree
        results (list of SastResult): results for the BFL node
        additional_properties (dict): the additional properties will be added if include-graph is set to true

    """
    id: str = None
    bfl: ResultNode = None
    results: List[SastResult] = None
    additional_properties: dict = None


def construct_bfl_tree(item):
    return BflTree(
        id=item.get("id"),
        bfl=construct_result_node(item.get("bfl")),
        results=[
            construct_sast_result(result) for result in item.get("results", [])
        ],
        additional_properties=item.get("additionalProperties")
    )
