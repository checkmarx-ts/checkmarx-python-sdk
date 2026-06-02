from CheckmarxPythonSDK.CxOne import (
    get_applications_overview,
    get_applications_overview_aggregate,
    get_applications_overview_count,
)


def test_get_applications_overview():
    result = get_applications_overview(limit=5)
    assert result is not None
    assert "applications" in result


def test_get_applications_overview_aggregate():
    result = get_applications_overview_aggregate(
        group_by_field=["criticality"]
    )
    assert result is not None
    assert "applicationsCounters" in result


def test_get_applications_overview_count():
    result = get_applications_overview_count()
    assert isinstance(result, int)
