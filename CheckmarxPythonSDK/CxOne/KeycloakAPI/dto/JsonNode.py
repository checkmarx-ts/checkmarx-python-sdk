class JsonNode:
    def __init__(self, array, big_decimal, big_integer, binary, boolean, container_node, double, empty, json_node_float,
                 floating_point_number, json_node_int, integral_number, long, missing_node, node_type, null, number,
                 json_node_object, pojo, short, textual, value_node):
        self.array = array
        self.bigDecimal = big_decimal
        self.bigInteger = big_integer
        self.binary = binary
        self.boolean = boolean
        self.containerNode = container_node
        self.double = double
        self.empty = empty
        self.float = json_node_float
        self.floatingPointNumber = floating_point_number
        self.int = json_node_int
        self.integralNumber = integral_number
        self.long = long
        self.missingNode = missing_node
        self.nodeType = node_type
        self.null = null
        self.number = number
        self.object = json_node_object
        self.pojo = pojo
        self.short = short
        self.textual = textual
        self.valueNode = value_node

    def __str__(self):
        return f"JsonNode(" \
               f"array={self.array} " \
               f"bigDecimal={self.bigDecimal} " \
               f"bigInteger={self.bigInteger} " \
               f"binary={self.binary} " \
               f"boolean={self.boolean} " \
               f"containerNode={self.containerNode} " \
               f"double={self.double} " \
               f"empty={self.empty} " \
               f"float={self.float} " \
               f"floatingPointNumber={self.floatingPointNumber} " \
               f"int={self.int} " \
               f"integralNumber={self.integralNumber} " \
               f"long={self.long} " \
               f"missingNode={self.missingNode} " \
               f"nodeType={self.nodeType} " \
               f"null={self.null} " \
               f"number={self.number} " \
               f"object={self.object} " \
               f"pojo={self.pojo} " \
               f"short={self.short} " \
               f"textual={self.textual} " \
               f"valueNode={self.valueNode} " \
               f")"

    def to_dict(self):
        return {
            "array": self.array,
            "bigDecimal": self.bigDecimal,
            "bigInteger": self.bigInteger,
            "binary": self.binary,
            "boolean": self.boolean,
            "containerNode": self.containerNode,
            "double": self.double,
            "empty": self.empty,
            "float": self.float,
            "floatingPointNumber": self.floatingPointNumber,
            "int": self.int,
            "integralNumber": self.integralNumber,
            "long": self.long,
            "missingNode": self.missingNode,
            "nodeType": self.nodeType,
            "null": self.null,
            "number": self.number,
            "object": self.object,
            "pojo": self.pojo,
            "short": self.short,
            "textual": self.textual,
            "valueNode": self.valueNode,
        }


def construct_json_node(item):
    return JsonNode(
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
