from dataclasses import dataclass


@dataclass
class ResultNode:
    column: int = None
    file_name: str = None
    full_name: str = None
    length: int = None
    line: int = None
    method_line: int = None
    method: str = None
    name: str = None
    dom_type: str = None
    node_hash: str = None

    @classmethod
    def from_dict(cls, item: dict) -> "ResultNode":
        return cls(
            column=item.get("column"),
            file_name=item.get("fileName"),
            full_name=item.get("fullName"),
            length=item.get("length"),
            line=item.get("line"),
            method_line=item.get("methodLine"),
            method=item.get("method"),
            name=item.get("name"),
            dom_type=item.get("domType"),
            node_hash=item.get("nodeHash"),
        )
