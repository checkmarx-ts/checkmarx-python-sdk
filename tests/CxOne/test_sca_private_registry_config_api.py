import pytest

from CheckmarxPythonSDK.CxOne import (
    associate_configurations_with_project,
    associate_configurations_with_tag,
    associate_projects_with_configuration,
    create_configuration,
    create_tag,
    delete_configuration,
    delete_tag,
    disassociate_configurations_from_project,
    disassociate_configurations_from_tag,
    get_all_configurations,
    get_configuration,
    get_configurations_by_tag,
    get_project_configurations,
    get_projects_by_configuration,
    get_projects_with_configurations,
    get_tags_with_configurations,
    update_configuration,
)
from CheckmarxPythonSDK.CxOne import ProjectsAPI as _ProjectsAPI
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


def test_delete_configuration():
    config_request = ScaRegistryConfigRequest(
        configurationName="tmp-delete-test-config",
        content=(
            '<?xml version="1.0" encoding="utf-8"?>\n'
            "<configuration>\n"
            '  <packageSources>\n'
            '    <add key="nuget.org" value="https://api.nuget.org/v3/index.json" />\n'
            '    <add key="Tmp" value="${{cx.test.url}}/tmp/" />\n'
            "  </packageSources>\n"
            "  <packageSourceCredentials>\n"
            "    <Tmp>\n"
            '      <add key="Username" value="${{cx.test.username}}" />\n'
            '      <add key="ClearTextPassword" value="${{cx.test.password}}" />\n'
            "    </Tmp>\n"
            "  </packageSourceCredentials>\n"
            "</configuration>"
        ),
        packageManager="nuget",
    )
    created = create_configuration(config_request)
    config_id = created.id

    result = delete_configuration(config_id)
    assert result is True


def test_update_configuration():
    # Create a config first
    create_req = ScaRegistryConfigRequest(
        configurationName="tmp-update-test-config",
        content=(
            '<?xml version="1.0" encoding="utf-8"?>\n'
            "<configuration>\n"
            '  <packageSources>\n'
            '    <add key="nuget.org" value="https://api.nuget.org/v3/index.json" />\n'
            "  </packageSources>\n"
            "</configuration>"
        ),
        packageManager="nuget",
    )
    created = create_configuration(create_req)
    config_id = created.id

    # Update it
    update_req = ScaRegistryConfigRequest(
        configurationName="tmp-update-test-config-modified",
        content=(
            '<?xml version="1.0" encoding="utf-8"?>\n'
            "<configuration>\n"
            '  <packageSources>\n'
            '    <add key="nuget.org" value="https://api.nuget.org/v3/index.json" />\n'
            '    <add key="Updated" value="${{cx.test.url}}/updated/" />\n'
            "  </packageSources>\n"
            "  <packageSourceCredentials>\n"
            "    <Updated>\n"
            '      <add key="Username" value="${{cx.test.username}}" />\n'
            '      <add key="ClearTextPassword" value="${{cx.test.password}}" />\n'
            "    </Updated>\n"
            "  </packageSourceCredentials>\n"
            "</configuration>"
        ),
        packageManager="nuget",
    )
    result = update_configuration(config_id, update_req)
    assert result is True

    # Verify the update
    updated = get_configuration(config_id)
    assert updated.configurationName == "tmp-update-test-config-modified"

    # Cleanup
    delete_configuration(config_id)


def _get_project_id():
    projects = _ProjectsAPI().get_a_list_of_projects(limit=1)
    if projects.projects:
        return projects.projects[0].id
    return None


def test_associate_configurations_with_project():
    project_id = _get_project_id()
    if not project_id:
        pytest.skip("No projects found")
    configs = get_all_configurations(page_number=1, page_size=1)
    if not configs:
        pytest.skip("No configurations found")
    config_id = configs[0].id

    try:
        result = associate_configurations_with_project(project_id, [config_id])
    except Exception as e:
        msg = str(e)
        if "400" in msg or "401" in msg or "403" in msg:
            pytest.skip("API returned client error: {}".format(msg))
        raise
    assert result is not None
    assert result.id is not None
    assert result.message is not None


def test_get_project_configurations():
    project_id = _get_project_id()
    if not project_id:
        pytest.skip("No projects found")
    result = get_project_configurations(project_id)
    assert result is not None
    assert isinstance(result, list)
    if result:
        config = result[0]
        assert config.id is not None
        assert config.configurationName is not None


def test_disassociate_configurations_from_project():
    project_id = _get_project_id()
    if not project_id:
        pytest.skip("No projects found")
    configs = get_all_configurations(page_number=1, page_size=1)
    if not configs:
        pytest.skip("No configurations found")
    config_id = configs[0].id

    try:
        associate_configurations_with_project(project_id, [config_id])
    except Exception as e:
        msg = str(e)
        if "400" in msg or "401" in msg or "403" in msg:
            pytest.skip("Associate API returned client error: {}".format(msg))
        raise

    result = disassociate_configurations_from_project(project_id, [config_id])
    assert result is True


def test_associate_configurations_with_tag():
    configs = get_all_configurations(page_number=1, page_size=1)
    if not configs:
        pytest.skip("No configurations found")
    config_id = configs[0].id

    tag = create_tag({"name": "tmp-assoc-test-tag"})
    tag_id = tag.get("id")

    try:
        result = associate_configurations_with_tag(tag_id, [config_id])
    except Exception as e:
        msg = str(e)
        delete_tag(tag_id)
        if "400" in msg or "401" in msg or "403" in msg:
            pytest.skip("API returned client error: {}".format(msg))
        raise

    assert result is not None
    assert result.id is not None
    assert result.message is not None

    delete_tag(tag_id)


def test_disassociate_configurations_from_tag():
    configs = get_all_configurations(page_number=1, page_size=1)
    if not configs:
        pytest.skip("No configurations found")
    config_id = configs[0].id

    tag = create_tag({"name": "tmp-disassoc-tag-test"})
    tag_id = tag.get("id")

    try:
        associate_configurations_with_tag(tag_id, [config_id])
    except Exception as e:
        delete_tag(tag_id)
        msg = str(e)
        if "400" in msg or "401" in msg or "403" in msg:
            pytest.skip("Associate API returned client error: {}".format(msg))
        raise

    result = disassociate_configurations_from_tag(tag_id)
    assert result is True

    delete_tag(tag_id)


def test_get_projects_with_configurations():
    result = get_projects_with_configurations(page_number=1, page_size=5)
    assert result is not None
    assert isinstance(result, list)
    if result:
        item = result[0]
        assert item.id is not None
        assert item.tenantId is not None


def test_get_projects_by_configuration():
    configs = get_all_configurations(page_number=1, page_size=1)
    if not configs:
        pytest.skip("No configurations found")
    config_id = configs[0].id

    result = get_projects_by_configuration(config_id)
    assert result is not None
    assert isinstance(result, list)


def test_associate_projects_with_configuration():
    project_id = _get_project_id()
    if not project_id:
        pytest.skip("No projects found")
    configs = get_all_configurations(page_number=1, page_size=1)
    if not configs:
        pytest.skip("No configurations found")
    config_id = configs[0].id

    try:
        result = associate_projects_with_configuration(config_id, [project_id])
    except Exception as e:
        msg = str(e)
        if "400" in msg or "401" in msg or "403" in msg:
            pytest.skip("API returned client error: {}".format(msg))
        raise
    assert result is not None
    assert result.id is not None
    assert result.message is not None


def test_get_configurations_by_tag():
    configs = get_all_configurations(page_number=1, page_size=1)
    if not configs:
        pytest.skip("No configurations found")
    config_id = configs[0].id

    tag = create_tag({"name": "tmp-get-by-tag-test"})
    tag_id = tag.get("id")

    try:
        associate_configurations_with_tag(tag_id, [config_id])
    except Exception as e:
        delete_tag(tag_id)
        msg = str(e)
        if "400" in msg or "401" in msg or "403" in msg:
            pytest.skip("Associate API returned client error: {}".format(msg))
        raise

    result = get_configurations_by_tag(tag_id)
    assert result is not None
    assert isinstance(result, list)

    delete_tag(tag_id)
