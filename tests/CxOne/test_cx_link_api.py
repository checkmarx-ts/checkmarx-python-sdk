import pytest

from CheckmarxPythonSDK.CxOne import (
    get_links,
    get_link,
    create_link,
    update_link,
    delete_link,
    recreate_link,
)


def test_get_links():
    result = get_links(limit=10)
    assert result is not None
    assert "items" in result


def test_create_update_recreate_delete_link():
    import datetime
    suffix = datetime.datetime.now().strftime("%H%M%S")
    link_name = "test-sdk-link-{}".format(suffix)

    # Create a link
    created = create_link(
        name=link_name,
        description="SDK test link",
        private_url="https://example.com/test",
    )
    assert created is not None
    link_id = created.get("link", {}).get("id")
    assert link_id is not None

    # GET by ID
    link = get_link(id=link_id)
    assert link is not None
    assert "name" in link

    # Update
    updated_name = "test-sdk-link-upd-{}".format(suffix)
    is_updated = update_link(
        id=link_id,
        name=updated_name,
        description="Updated description",
    )
    assert is_updated is True

    # Recreate
    recreated = recreate_link(id=link_id)
    assert recreated is not None
    assert "link" in recreated
    assert "token" in recreated

    # Delete
    is_deleted = delete_link(id=link_id)
    assert is_deleted is True
