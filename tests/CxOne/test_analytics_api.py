from CheckmarxPythonSDK.CxOne import query_kpi


def test_query_kpi():
    result = query_kpi(body={
        "kpi": "vulnerabilitiesBySeverityTotal",
    })
    assert result is not None
    assert "distribution" in result or "total" in result
