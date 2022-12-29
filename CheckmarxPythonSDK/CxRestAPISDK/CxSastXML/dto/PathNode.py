from .Snippet import Snippet


class PathNode:
    def __init__(self, file_name, line_number, column_number, node_id, node_name, node_type, node_name_length,
                 snippet=None):
        """

        Args:
            file_name (str):
            line_number (int):
            column_number (int):
            node_id (int):
            node_name (str):
            node_type (str):
            node_name_length (int):
            snippet (Snippet):
        """
        self.FileName = file_name
        self.Line = line_number
        self.Column = column_number
        self.NodeId = node_id
        self.Name = node_name
        self.Type = node_type
        self.Length = node_name_length
        self.Snippet = snippet

    def __str__(self):
        return "PathNode(file_name={file_name}, line_number={line_number}, column_number={column_number}, " \
               "node_id={node_id}, node_name={node_name}, node_type={node_type}, " \
               "node_name_length={node_name_length}, " \
               "snippet={snippet})".format(
                    file_name=self.FileName,
                    line_number=self.Line,
                    column_number=self.Column,
                    node_id=self.NodeId,
                    node_name=self.Name,
                    node_type=self.Type,
                    node_name_length=self.Length,
                    snippet=self.Snippet
                )


def construct_path_node(file_name, line_number, column_number, node_id, node_name, node_type, node_name_length,
                        snippet):
    return PathNode(
            file_name=file_name,
            line_number=int(line_number),
            column_number=int(column_number),
            node_id=int(node_id),
            node_name=node_name,
            node_type=node_type,
            node_name_length=int(node_name_length),
            snippet=snippet
        )
