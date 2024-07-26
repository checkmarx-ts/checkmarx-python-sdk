from CheckmarxPythonSDK.CxOne import (
    get_allowed_and_current_contributors_for_the_current_tenant,
    get_contributors_details_for_current_tenant_exported_in_csv,
)


def test_get_allowed_and_current_contributors_for_the_current_tenant():
    result = get_allowed_and_current_contributors_for_the_current_tenant()
    assert result is not None


def test_get_contributors_details_for_current_tenant_exported_in_csv():
    result = get_contributors_details_for_current_tenant_exported_in_csv()
    assert result is not None
