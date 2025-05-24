
class Predicate(object):
    def __init__(self, id: str = None, similarity_id: str = None, project_id: str = None,
                 severity: str = None, state: str = None, comment: str = None,
                 created_by: str = None, created_at: str = None, change_origin_type: int = None,
                 change_origin_name: str = None):
        self.ID = id
        self.similarityId = similarity_id
        self.projectId = project_id
        self.severity = severity
        self.state = state
        self.comment = comment
        self.createdBy = created_by
        self.createdAt = created_at
        self.changeOriginType = change_origin_type
        self.changeOriginName = change_origin_name

    def __str__(self):
        return (f"Predicate(ID={self.ID}, similarityId={self.similarityId}, projectId={self.projectId}, "
                f"severity={self.severity}, state={self.state}, comment={self.comment}, createdBy={self.createdBy}, "
                f"createdAt={self.createdAt}, changeOriginType={self.changeOriginType}, "
                f"changeOriginName={self.changeOriginName})")
