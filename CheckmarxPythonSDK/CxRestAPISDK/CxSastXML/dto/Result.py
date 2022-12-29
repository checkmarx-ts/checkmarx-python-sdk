from .Path import Path


class Result:
    def __init__(self, node_id, file_name, status, line_number, column_number, false_positive, severity, assign_to_user,
                 state, remark, deeplink, severity_index, status_index, detection_date, path=None):
        """

        Args:
            node_id (int):
            file_name (str):
            status (str):
            line_number (int):
            column_number (int):
            false_positive (str):
            severity (str):
            assign_to_user (str):
            state (int):
            remark (str):
            deeplink (str):
            severity_index (int):
            status_index (int):
            detection_date (str):
            path (Path):
        """
        self.NodeId = node_id
        self.FileName = file_name
        self.Status = status
        self.Line = line_number
        self.Column = column_number
        self.FalsePositive = false_positive
        self.Severity = severity
        self.AssignToUser = assign_to_user
        self.State = state
        self.Remark = remark
        self.DeepLink = deeplink
        self.SeverityIndex = severity_index
        self.StatusIndex = status_index
        self.DetectionDate = detection_date
        self.Path = path

    def __str__(self):
        return "Result(node_id={node_id}, file_name={file_name}, status={status}, line_number={line_number}, "\
               "column_number={column_number}, false_positive={false_positive}, severity={severity}, "\
               "assign_to_user={assign_to_user}, state={state}, remark={remark}, deeplink={deeplink}, "\
               "severity_index={severity_index}, status_index={status_index}, detection_date={detection_date}, "\
               "path={path})".format(
                    node_id=self.NodeId,
                    file_name=self.FileName,
                    status=self.Status,
                    line_number=self.Line,
                    column_number=self.Column,
                    false_positive=self.FalsePositive,
                    severity=self.Severity,
                    assign_to_user=self.AssignToUser,
                    state=self.State,
                    remark=self.Remark,
                    deeplink=self.DeepLink,
                    severity_index=self.SeverityIndex,
                    status_index=self.StatusIndex,
                    detection_date=self.DetectionDate,
                    path=self.Path
                )


def construct_result(item, path=None):
    return Result(
        node_id=int(item.get("NodeId")),
        file_name=item.get("FileName"),
        status=item.get("Status"),
        line_number=int(item.get("Line")),
        column_number=int(item.get("Column")),
        false_positive=item.get("FalsePositive"),
        severity=item.get("Severity"),
        assign_to_user=item.get("AssignToUser"),
        state=item.get("State"),
        remark=item.get("Remark"),
        deeplink=item.get("DeepLink"),
        severity_index=int(item.get("SeverityIndex")),
        status_index=int(item.get("StatusIndex")),
        detection_date=item.get("DetectionDate"),
        path=path
    )
