from dataclasses import dataclass


@dataclass
class MethodParameter:
    """

    Args:
        name (str):
        label (str):
        documentation (str):
    """
    name: str
    label: str
    documentation: str


def construct_method_parameter(item):
    return MethodParameter(
        name=item.get("name"),
        label=item.get("label"),
        documentation=item.get("documentation")
    )
