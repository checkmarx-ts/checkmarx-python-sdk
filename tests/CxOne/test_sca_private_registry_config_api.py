import pytest

from CheckmarxPythonSDK.CxOne import (
    create_configuration,
    get_all_configurations,
    get_configuration,
)
from CheckmarxPythonSDK.CxOne.dto import ScaRegistryConfigRequest


def test_get_all_configurations():
    try:
        result = get_all_configurations(page_number=1, page_size=5)
    except Exception as e:
        msg = str(e)
        if "400" in msg or "401" in msg or "403" in msg or "404" in msg:
            pytest.skip("API returned client error: {}".format(msg))
        raise
    assert result is not None
    assert isinstance(result, list)
    if result:
        config = result[0]
        assert config.id is not None
        assert config.configurationName is not None


def test_create_configuration():
    config_request = ScaRegistryConfigRequest(
        configurationName="test-nuget-config",
        content=(
            '<?xml version="1.0" encoding="utf-8"?>\n'
            "<configuration>\n"
            '  <packageSources>\n'
            '    <add key="nuget.org" value="https://api.nuget.org/v3/index.json" />\n'
            '    <add key="TestServer" value="${{cx.test.url}}/artifactory/api/nuget/v3/test/" />\n'
            "  </packageSources>\n"
            "  <packageSourceCredentials>\n"
            "    <TestServer>\n"
            '      <add key="Username" value="${{cx.test.username}}" />\n'
            '      <add key="ClearTextPassword" value="${{cx.test.password}}" />\n'
            "    </TestServer>\n"
            "  </packageSourceCredentials>\n"
            "</configuration>"
        ),
        packageManager="nuget",
    )
    try:
        result = create_configuration(config_request)
    except Exception as e:
        msg = str(e)
        if "400" in msg or "401" in msg or "403" in msg:
            pytest.skip("API returned client error: {}".format(msg))
        raise
    assert result is not None
    assert result.id is not None
    assert result.message is not None


def test_get_configuration():
    configs = get_all_configurations(page_number=1, page_size=1)
    if not configs:
        pytest.skip("No configurations found")
    config_id = configs[0].id
    result = get_configuration(config_id)
    assert result is not None
    assert result.id == config_id
    assert result.configurationName is not None
    assert result.tenantId is not None
    assert result.content is not None
    assert result.packageManager is not None
    assert result.lastUpdate is not None
