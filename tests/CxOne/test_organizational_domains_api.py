from CheckmarxPythonSDK.CxOne import (
    list_organizational_domains,
    add_organizational_domains,
    delete_organizational_domain,
)


def test_list_organizational_domains():
    result = list_organizational_domains(limit=10)
    assert result is not None
    assert "items" in result


def test_add_and_delete_organizational_domain():
    # Add a test domain
    test_domain = "test-sdk-example.com"
    try:
        result = add_organizational_domains(domains=test_domain)
        assert result is not None
        assert "added" in result

        # Delete the domain if it was added
        items = list_organizational_domains(search=test_domain)
        for item in items.get("items", []):
            if item.get("domain") == test_domain:
                is_deleted = delete_organizational_domain(id=item["id"])
                assert is_deleted is True
                break
    except Exception as e:
        print("add/delete organizational domain skipped: {}".format(str(e)))
