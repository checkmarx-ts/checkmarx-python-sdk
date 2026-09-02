from unittest.mock import MagicMock

from CheckmarxPythonSDK.CxOne.aiTriageAPI import AiTriageAPI


def _api_client(json_body=None):
    client = MagicMock()
    client.configuration.server_base_url = "https://example.com"
    response = MagicMock()
    response.json.return_value = json_body or {}
    client.call_api.return_value = response
    return client


class TestRetrieveAiTriageResults:

    def test_group_id_with_hash_characters_is_url_encoded(self):
        """group_id values like SCA group ids ("CVE-...#-#pkg#-#uuid") must be
        percent-encoded before being substituted into the path, otherwise the
        '#' is treated as a URL fragment separator and the request 404s.
        """
        client = _api_client()
        api = AiTriageAPI(api_client=client)
        group_id = (
            "CVE-2015-4852#-#Maven-commons-collections:commons-collections-"
            "3.2.1#-#2db0b158-3068-4d7e-86e6-0d922f22a69c"
        )

        api.retrieve_ai_triage_results(project_id="proj-1", group_id=group_id)

        called_url = client.call_api.call_args.kwargs["url"]
        assert "#" not in called_url
        assert called_url == (
            "https://example.com/api/ai-triage/triage/proj-1/"
            "CVE-2015-4852%23-%23Maven-commons-collections%3Acommons-"
            "collections-3.2.1%23-%232db0b158-3068-4d7e-86e6-0d922f22a69c"
        )

    def test_group_id_without_reserved_characters_is_unchanged(self):
        client = _api_client()
        api = AiTriageAPI(api_client=client)

        api.retrieve_ai_triage_results(project_id="proj-1", group_id="12345")

        called_url = client.call_api.call_args.kwargs["url"]
        assert called_url == "https://example.com/api/ai-triage/triage/proj-1/12345"
