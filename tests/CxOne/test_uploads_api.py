from CheckmarxPythonSDK.CxOne import (
    create_a_pre_signed_url_to_upload_files,
    upload_zip_content_for_scanning
)


def test_create_a_pre_signed_url_to_upload_files():
    url = create_a_pre_signed_url_to_upload_files()
    print("url: {}".format(url))
    assert url is not None
    result = upload_zip_content_for_scanning(
        upload_link=url,
        zip_file_path=r"/tests/JavaVulnerableLab-master.zip"
    )
    assert result is True
