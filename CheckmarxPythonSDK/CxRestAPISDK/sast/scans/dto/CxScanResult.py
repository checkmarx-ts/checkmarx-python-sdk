# encoding: utf-8

class CxScanResult:

    class Node:

        def __init__(self, node_id, full_name, short_name, file_name, line,
                     column, length, remarks, method_line):
            """
            Args:
                node_id (int):
                full_name (str):
                short_name (str):
                file_name (str):
                line (int):
                column (int):
                length (int):
                remarks (str):
                method_line (int):
            """
            self.node_id = node_id
            self.full_name = full_name
            self.short_name = short_name
            self.file_name = file_name
            self.line = line
            self.column = column
            self.length = length
            self.remarks = remarks
            self.method_line = method_line

        @staticmethod
        def from_dict(d):
            """
            Args:
                d (dict): a dict containing the node data
            """
            return CxScanResult.Node(
                node_id=d.get('nodeId'),
                full_name=d.get('fullName'),
                short_name=d.get('shortName'),
                file_name=d.get('fileName'),
                line=d.get('line'),
                column=d.get('column'),
                length=d.get('length'),
                remarks=d.get('remarks'),
                method_line=d.get('methodLine')
            )

        def __str__(self):
            return """CxScanResult.Node(node_id={}, full_name={},
            short_name={}, file_name={}, line={}, column={}, length={},
            remarks={}, method_line={})""".format(self.node_id,
                                                  self.full_name,
                                                  self.short_name,
                                                  self.file_name,
                                                  self.line,
                                                  self.column,
                                                  self.length,
                                                  self.remarks,
                                                  self.method_line)

    class Query:

        def __init__(self, query_version_id, query_id, name, severity,
                     categories, cwe):
            """
            Args:
                query_version_id (int):
                query_id (int):
                name (str):
                severity (int):
                categories (str):
                cwe (int):
            """
            self.query_version_id = query_version_id
            self.query_id = query_id
            self.name = name
            self.severity = severity
            self.categories = categories
            self.cwe = cwe

        @staticmethod
        def from_dict(d):
            """
            Args:
                d (dict): a dict containing the query data
            """
            return CxScanResult.Query(
                query_version_id=d.get('queryVersionId'),
                query_id=d.get('queryId'),
                name=d.get('name'),
                severity=d.get('severity'),
                categories=d.get('categories'),
                cwe=d.get('cwe')
            )

        def __str__(self):
            return """CxScanResult.Query(query_version_id={}, query_id={}, name={},
            severity={}, categories={}, cwe={})""".format(
                self.query_version_id, self.query_id, self.name, self.severity,
                self.categories, self.cwe
            )

    class Snippet:

        def __init__(self, file_name, line, code):
            """
            Args:
                file_name (str):
                line (int):
                code (str):
            """
            self.file_name = file_name
            self.line = line
            self.code = code

        @staticmethod
        def from_dict(d):
            """
            Args:
                d (dict): dict containing the snippet data
            """
            return CxScanResult.Snippet(
                file_name=d.get('fileName'),
                line=d.get('line'),
                code=d.get('code')
            )

        def __str__(self):
            return "CxScanResult.Snippet(file_name={}, line={}, code={})".format(
                self.file_name, self.line, self.code
            )

    def __init__(self, index, path_id, similarity_hash, date, detection_date,
                 confidence_level, cx_rank, bfl_node_short_name, bfl_node_id,
                 severity, state, status, assigned_to_user_id, assigned_to,
                 comment, deep_link, query, source_snippet, sink_snippet,
                 nodes, lcid, cx_description_id, result_description,
                 best_fix_location, risk, cause, general_recommendations):
        """
        Args:
            index (int):
            path_id (int):
            similarity_hash (int)
            date (str):
            detection_date (str):
            confidence_level (int):
            cx_rank (float):
            bfl_node_short_name (str):
            bfl_node_id (int):
            severity (int):
            status (int):
            assigned_to_user_id (int):
            assigned_to_user (str):
            comment (str):
            deep_link (str):
            query (:obj:`CxQuery`)
            source_snippet (:obj:`CxSnippet`):
            sink_snippet (:obj:`CxSnippet`)
            nodes: (list of `CxScanResultNode`)
            lcid (int):
            cx_description_id (int):
            result_description (str):
            best_fix_location (str):
            risk (str):
            cause (str):
            general_recommendations (str):
        """
        self.index = index
        self.path_id = path_id
        self.similarity_hash = similarity_hash
        self.date = date
        self.detection_date = detection_date
        self.confidence_level = confidence_level
        self.cx_rank = cx_rank
        self.bfl_node_short_name = bfl_node_short_name
        self.bfl_node_id = bfl_node_id
        self.severity = severity
        self.state = state
        self.status = status
        self.assigned_to_user_id = assigned_to_user_id
        self.assigned_to = assigned_to
        self.comment = comment
        self.deep_link = deep_link
        self.query = query
        self.source_snippet = source_snippet
        self.sink_snippet = sink_snippet
        self.nodes = nodes
        self.lcid = lcid
        self.cx_description_id = cx_description_id
        self.result_description = result_description
        self.best_fix_location = best_fix_location
        self.risk = risk
        self.cause = cause
        self.general_recommendations = general_recommendations

    @staticmethod
    def from_dict(d):
        """
        Args:
            d (`dict` of :obj:): a dictionary containin the result data
        """
        nodes = [CxScanResult.Node.from_dict(d2) for d2 in d.get('nodes')]
        return CxScanResult(index=d.get('index'),
                        path_id=d.get('pathId'),
                        similarity_hash=d.get('similarityHash'),
                        date=d.get('date'),
                        detection_date=d.get('detectionDate'),
                        confidence_level=d.get('confidenceLevel'),
                        cx_rank=d.get('cxRank'),
                        bfl_node_short_name=d.get('bflNodeShortName'),
                        bfl_node_id=d.get('bflNodeId'),
                        severity=d.get('severity'),
                        state=d.get('state'),
                        status=d.get('status'),
                        assigned_to_user_id=d.get('assignedToUserId'),
                        assigned_to=d.get('assignedTo'),
                        comment=d.get('comment'),
                        deep_link=d.get('deepLink'),
                        query=CxScanResult.Query.from_dict(d.get('query')),
                        source_snippet=CxScanResult.Snippet.from_dict(
                            d.get('sourceSnippet')),
                        sink_snippet=CxScanResult.Snippet.from_dict(
                            d.get('sinkSnippet')),
                        nodes=nodes,
                        lcid=d.get('lcid'),
                        cx_description_id=d.get('cxDescriptionID'),
                        result_description=d.get('resultDescription'),
                        best_fix_location=d.get('bestFixLocation'),
                        risk=d.get('risk'),
                        cause=d.get('cause'),
                        general_recommendations=d.get('generalRecommendations')
                        )

    def __str__(self):
        return """CxScanResult(index={}, path_id={}, similarity_hash={},
        date={}, detection_date={}, confidence_level={}, cx_rank={},
        bfl_node_short_name={}, bfl_node_id={}, severity={}, state={},
        status={}, assigned_to_user_id={}, assigned_to={}, comment={},
        deep_link={}, query={}, source_snippet={}, sink_snippet={}, nodes={},
        lcid={}, cx_description_id={}, result_description={},
        best_fix_location={}, risk={}, cause={},
        general_recommendations={}""".format(self.index,
                                             self.path_id,
                                             self.similarity_hash,
                                             self.date,
                                             self.detection_date,
                                             self.confidence_level,
                                             self.cx_rank,
                                             self.bfl_node_short_name,
                                             self.bfl_node_id,
                                             self.severity,
                                             self.state,
                                             self.status,
                                             self.assigned_to_user_id,
                                             self.assigned_to,
                                             self.comment,
                                             self.deep_link,
                                             self.query,
                                             self.source_snippet,
                                             self.sink_snippet,
                                             self.nodes,
                                             self.lcid,
                                             self.cx_description_id,
                                             self.result_description,
                                             self.best_fix_location,
                                             self.risk,
                                             self.cause,
                                             self.general_recommendations)
