from CheckmarxPythonSDK.CxAST import (
    create_a_pre_signed_url_to_upload_files
)


def test_create_a_pre_signed_url_to_upload_files():
    url = create_a_pre_signed_url_to_upload_files()
    assert url is not None
