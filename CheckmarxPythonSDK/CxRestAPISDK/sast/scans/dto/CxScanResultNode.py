class CxScanResultNode(object):

    def __init__(self, node_id, order, short_name, full_name, file_name, folder, line, column, length, method_line,
                 source_url):
        """

        Args:
            node_id (int):
            order (int):
            short_name (str):
            full_name (str):
            file_name (str):
            folder (str):
            line (int):
            column (int):
            length (int):
            method_line (int):
            source_url (str):
        """
        self.id = node_id
        self.order = order
        self.short_name = short_name
        self.full_name = full_name
        self.file_name = file_name
        self.folder = folder
        self.line = line
        self.column = column
        self.length = length
        self.method_line = method_line
        self.source_url = source_url

    def __str__(self):
        return """CxScanResultNode(id={}, order={}, short_name={}, full_name={}, file_name={}, folder={}, 
        line={}, column={}, length={}, method_line={}, source_url={})""".format(
            self.id, self.order, self.short_name, self.full_name, self.file_name, self.folder,
            self.line, self.column, self.length, self.method_line, self.source_url
        )
