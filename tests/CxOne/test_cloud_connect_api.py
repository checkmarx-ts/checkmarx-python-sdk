from CheckmarxPythonSDK.CxOne import get_cloud_connections
from CheckmarxPythonSDK.CxOne.dto import CloudConnectionsResponse


def test_get_cloud_connections():
    result = get_cloud_connections()
    assert isinstance(result, CloudConnectionsResponse)
    assert result.total_count is not None
    assert result.total_filtered_count is not None
    assert isinstance(result.cloud_connections, list)


def test_get_cloud_connections_with_pagination_and_filter():
    result = get_cloud_connections(limit=5, offset=0, filter_="does-not-exist")
    assert isinstance(result, CloudConnectionsResponse)
    assert result.total_filtered_count == 0
    assert result.cloud_connections == []
