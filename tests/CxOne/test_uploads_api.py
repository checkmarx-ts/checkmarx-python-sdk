from CheckmarxPythonSDK.CxOne import (
    create_a_pre_signed_url_to_upload_files,
    upload_zip_content_for_scanning
)


def test_create_a_pre_signed_url_to_upload_files():
    url = create_a_pre_signed_url_to_upload_files()
    print("url: {}".format(url))
    assert url is not None
    # """https://eu.ast.checkmarx.net/storage/uploads.ireland.eu-west-1-602005780816/014c234f-01ad-4233-a89b-9ac6d4ce94c4/252708f4-b033-47d1-9c80-125f29bdde60?X-Amz-Algorithm=AWS4-HMAC-SHA256&X-Amz-Credential=ast%2F20240823%2Fus-east-1%2Fs3%2Faws4_request&X-Amz-Date=20240823T043959Z&X-Amz-Expires=86400&X-Amz-Signature=7b6bd6dc015984c38ce02f5a2d8844f19b74e86a7b98a1eb395063d0b441a26e&X-Amz-SignedHeaders=host"""
    result = upload_zip_content_for_scanning(
        upload_link=url,
        zip_file_path=r"D:\HappyYang\SourceCode\GitHub\ZIP FILES\jvl.zip"
    )
    assert result is True
