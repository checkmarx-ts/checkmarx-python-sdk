import urllib.request

from CheckmarxPythonSDK.CxOne import (
    create_a_pre_signed_url_to_upload_files,
    upload_zip_content_for_scanning,
    start_multipart_upload,
    get_multipart_presigned_url,
    complete_multipart_upload,
    abort_multipart_upload,
)


def test_create_a_pre_signed_url_to_upload_files():
    zip_file_path = "/tmp/JavaVulnerableLab-master.zip"
    urllib.request.urlretrieve(
        "https://github.com/CSPF-Founder/JavaVulnerableLab/archive/refs/heads/master.zip",
        zip_file_path,
    )
    url = create_a_pre_signed_url_to_upload_files()
    print("url: {}".format(url))
    assert url is not None
    result = upload_zip_content_for_scanning(
        upload_link=url,
        zip_file_path=zip_file_path,
    )
    assert result is True


def test_multipart_upload_flow():
    """Test the full multipart upload lifecycle: start -> presigned -> abort."""
    # Start multipart upload
    start_result = start_multipart_upload(file_size=1024 * 1024)
    assert start_result is not None
    upload_id = start_result.get("UploadID")
    object_name = start_result.get("objectName")
    assert upload_id is not None
    assert object_name is not None

    # Get presigned URL for a part
    presigned = get_multipart_presigned_url(
        upload_id=upload_id, part_number=1, object_name=object_name
    )
    assert presigned is not None
    assert "presignedURL" in presigned

    # Abort (clean up — can't actually complete without uploading parts)
    is_aborted = abort_multipart_upload(
        upload_id=upload_id, object_name=object_name
    )
    assert is_aborted is True
