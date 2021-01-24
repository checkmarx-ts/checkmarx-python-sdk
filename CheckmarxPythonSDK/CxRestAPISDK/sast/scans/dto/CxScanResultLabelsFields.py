class CxScanResultLabelsFields(object):

    def __init__(self, state, severity, user_assignment, comment):
        self.state = state
        self.severity = severity
        self.user_assignment = user_assignment
        self.comment = comment

    def __str__(self):
        return "CxScanResultLabelsFields(state={}, severity={}, user_assignment={], comment={})".format(
            self.state, self.severity, self.user_assignment, self.comment
        )
