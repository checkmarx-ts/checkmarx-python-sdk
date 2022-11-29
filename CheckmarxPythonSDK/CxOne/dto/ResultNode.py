class ResultNode(object):
    def __init__(self, column, file_name, full_name, length, line, method_line, method, name, dom_type, node_hash=None):
        """

        Args:
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
        self.column = column
        self.fileName = file_name
        self.fullName = full_name
        self.length = length
        self.line = line
        self.methodLine = method_line
        self.method = method
        self.name = name
        self.domType = dom_type
        self.nodeHash = node_hash

    def __str__(self):
        return """ResultNode(column={}, fileName={}, fullName={}, length={}, line={}, methodLine={}, method={}, name={},
        domType={}, nodeHash={})""".format(
            self.column, self.fileName, self.fullName, self.length, self.line, self.methodLine, self.method, self.name,
            self.domType, self.nodeHash
        )
