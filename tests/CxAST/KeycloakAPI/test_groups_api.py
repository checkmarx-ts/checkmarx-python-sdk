from CheckmarxPythonSDK.CxAST import (
    get_group_hierarchy
)


realm = "asean_2021_08"


def test_get_group_hierarchy():
    groups = get_group_hierarchy(realm=realm)
    assert groups is not None
