from CheckmarxPythonSDK.CxOne import (
    WebHookAPI,
    get_webhook_by_id,
    create_a_webhook_on_project,
    delete_webhook_by_id,
)
from CheckmarxPythonSDK.CxOne import ProjectsAPI as _ProjectsAPI
from CheckmarxPythonSDK.CxOne.dto import WebHookInput


def test_webhook_api():
    response = WebHookAPI().get_a_list_of_webhooks_related_to_tenant(limit=100)
    assert response.total_count >= 0


def test_get_webhook_by_id():
    """GET /api/webhooks/{id} — get a webhook by ID."""
    response = WebHookAPI().get_a_list_of_webhooks_related_to_tenant(limit=100)
    webhooks = response.webhooks
    if not webhooks:
        print("No webhooks found, skipping get_webhook_by_id")
        return
    webhook_id = webhooks[0].id
    webhook = get_webhook_by_id(webhook_id=webhook_id)
    assert webhook is not None
    assert webhook.id == webhook_id


def test_create_a_webhook_on_project():
    """POST /api/webhooks/projects/{project-id} — create then delete."""
    projects = _ProjectsAPI().get_a_list_of_projects(limit=1)
    if not projects.projects:
        print("No projects found, skipping create webhook on project")
        return
    project_id = projects.projects[0].id

    webhook_input = WebHookInput(
        name="test-sdk-webhook",
        active=False,
        enabledEvents=["scan_completed_successfully"],
        config={"url": "https://example.com/webhook"},
    )
    webhook = create_a_webhook_on_project(
        project_id=project_id, webhook_input=webhook_input
    )
    assert webhook is not None
    assert webhook.id is not None

    # Clean up
    is_deleted = delete_webhook_by_id(webhook_id=webhook.id)
    assert is_deleted is True
