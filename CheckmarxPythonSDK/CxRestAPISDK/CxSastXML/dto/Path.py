from .PathNode import PathNode


class Path:
    def __init__(self, result_id, path_id, similarity_id, source_method, destination_method, path_nodes=None):
        """

        Args:
            result_id (int):
            path_id (int):
            similarity_id (int):
            source_method (str):
            destination_method (str):
            path_nodes (list of PathNode):
        """
        self.ResultId = result_id
        self.PathId = path_id
        self.SimilarityId = similarity_id
        self.SourceMethod = source_method
        self.DestinationMethod = destination_method
        self.PathNodes = path_nodes

    def __str__(self):
        return "Path(result_id={result_id}, path_id={path_id}, similarity_id={similarity_id}, "\
               "source_method={source_method}, destination_method={destination_method}, "\
               "path_nodes={path_nodes})".format(
                    result_id=self.ResultId, path_id=self.PathId, similarity_id=self.SimilarityId,
                    source_method=self.SourceMethod, destination_method=self.DestinationMethod,
                    path_nodes=self.PathNodes
                )


def construct_path(item, path_nodes=None):
    return Path(
            result_id=int(item.get("ResultId")),
            path_id=int(item.get("PathId")),
            similarity_id=int(item.get("SimilarityId")),
            source_method=item.get("SourceMethod"),
            destination_method=item.get("DestinationMethod"),
            path_nodes=path_nodes
        )
