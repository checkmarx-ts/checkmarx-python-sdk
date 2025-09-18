from CheckmarxPythonSDK.CxOne import WebHookAPI


def test_webhook_api():
    response = WebHookAPI().get_a_list_of_webhooks_related_to_tenant(limit=100)
    assert response.total_count == 0
