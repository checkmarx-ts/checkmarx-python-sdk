class ChangeDetails(object):

    def __init__(self, engine_version_changed, engine_version_changed_details, query_changed, query_changed_details,
                 code_change, code_change_details):
        """

        Args:
            engine_version_changed (booL):
            engine_version_changed_details (str):
            query_changed (bool):
            query_changed_details (str):
            code_change (bool):
            code_change_details (str):
        """
        self.engine_version_changed = engine_version_changed
        self.engine_version_changed_details = engine_version_changed_details
        self.query_changed = query_changed
        self.query_changed_details = query_changed_details
        self.code_change = code_change
        self.code_change_details = code_change_details

    def __str__(self):
        return f"""ChangeDetails(
        engine_version_changed={self.engine_version_changed},
        engine_version_changed_details={self.engine_version_changed_details},
        query_changed={self.query_changed},
        query_changed_details={self.query_changed_details},
        code_change={self.code_change},
        code_change_details={self.code_change_details},
        )"""


def construct_change_details(detail):
    return ChangeDetails(
            engine_version_changed=detail.get("engineVersionChanged"),
            engine_version_changed_details=detail.get("engineVersionChangeDetails"),
            query_changed=detail.get("queryChanged"),
            query_changed_details=detail.get("queryChangeDetails"),
            code_change=detail.get("codeChanged"),
            code_change_details=detail.get("codeChangeDetails")
        )
