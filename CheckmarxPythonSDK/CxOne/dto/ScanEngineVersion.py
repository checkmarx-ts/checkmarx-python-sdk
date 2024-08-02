class ScanEngineVersion(object):

    def __init__(self, scan_id, project_id, tenant_id, engine_version):
        """

        Args:
            scan_id:
            project_id:
            tenant_id:
            engine_version:
        """
        self.scan_id = scan_id
        self.project_id = project_id
        self.tenant_id = tenant_id
        self.engine_version = engine_version

    def __str__(self):
        return """ScanEngineVersion(
        scan_id={self.scan_id},
        project_id={self.project_id},
        tenant_id={self.tenant_id},
        engine_version={self.engine_version},
        )"""
