from dataclasses import dataclass


@dataclass
class JsonNode:
    array: ... = None
    big_decimal: ... = None
    big_integer: ... = None
    binary: ... = None
    boolean: ... = None
    container_node: ... = None
    double: ... = None
    empty: ... = None
    json_node_float: ... = None
    floating_point_number: ... = None
    json_node_int: ... = None
    integral_number: ... = None
    long: ... = None
    missing_node: ... = None
    node_type: ... = None
    null: ... = None
    number: ... = None
    json_node_object: ... = None
    pojo: ... = None
    short: ... = None
    textual: ... = None
    value_node: ... = None

    @classmethod
    def from_dict(cls, item: dict) -> "JsonNode":
        return cls(
            array=item.get("array"),
            big_decimal=item.get("bigDecimal"),
            big_integer=item.get("bigInteger"),
            binary=item.get("binary"),
            boolean=item.get("boolean"),
            container_node=item.get("containerNode"),
            double=item.get("double"),
            empty=item.get("empty"),
            json_node_float=item.get("float"),
            floating_point_number=item.get("floatingPointNumber"),
            json_node_int=item.get("int"),
            integral_number=item.get("integralNumber"),
            long=item.get("long"),
            missing_node=item.get("missingNode"),
            node_type=item.get("nodeType"),
            null=item.get("null"),
            number=item.get("number"),
            json_node_object=item.get("object"),
            pojo=item.get("pojo"),
            short=item.get("short"),
            textual=item.get("textual"),
            value_node=item.get("valueNode"),
        )
