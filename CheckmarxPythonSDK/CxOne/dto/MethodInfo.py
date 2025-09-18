from dataclasses import dataclass
from typing import List
from .MethodParameter import MethodParameter, construct_method_parameter


@dataclass
class MethodInfo:
    """

    Attributes:
        lang (str):
        name (str):
        member_of (str):
        documentation (str):
        return_type (str):
        kind (str):
        parameters (list of MethodParameter):
    """
    lang: str
    name: str
    member_of: str
    documentation: str
    return_type: str
    kind: str
    parameters: List[MethodParameter]


def construct_method_info(item):
    return MethodInfo(
        lang=item.get("lang"),
        name=item.get("name"),
        member_of=item.get("memberOf "),
        documentation=item.get("documentation"),
        return_type=item.get("returnType"),
        kind=item.get("kind"),
        parameters=[
            construct_method_parameter(method_param) for method_param in item.get("parameters", [])
        ]
    )
