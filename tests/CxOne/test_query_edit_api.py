from CheckmarxPythonSDK.CxOne import (
    create_new_audit_session,
)


def test_create_new_audit_session():
    project_id = "f6ec7d66-83bb-4228-88d0-67d64b98250f"
    scan_id = "440e9ad4-37d3-44a1-9617-bd8b089cb2c3"
    upload_url = "https://eu.ast.checkmarx.net/storage/uploads.ireland.eu-west-1-602005780816/014c234f-01ad-4233-a89b-9ac6d4ce94c4/938887cc-bfeb-49f5-b56e-7cf13bf2e3fe?X-Amz-Algorithm=AWS4-HMAC-SHA256&X-Amz-Credential=ast%2F20240605%2Fus-east-1%2Fs3%2Faws4_request&X-Amz-Date=20240605T032834Z&X-Amz-Expires=86400&X-Amz-Signature=6223157ba272f2268efeef8a8a1460bb9fe29228900523a8b41a39bcce21ce71&X-Amz-SignedHeaders=host"
    result = create_new_audit_session(project_id, scan_id, upload_url)
    assert result is not None