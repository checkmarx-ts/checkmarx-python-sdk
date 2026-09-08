import re

from CheckmarxPythonSDK.CxOne import VersionsAPI


def test_versions_api():
    response = VersionsAPI().get_versions_from_engines()
    # The engine versions are upgraded server-side on a different schedule
    # than this repo, so assert the shape instead of a specific release.
    assert re.fullmatch(r"\d+\.\d+\.\d+", response.sast), (
        f"unexpected SAST version format: {response.sast!r}"
    )
