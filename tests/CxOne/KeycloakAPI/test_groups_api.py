from CheckmarxPythonSDK.CxOne.KeycloakAPI import (
    get_group_hierarchy,
    create_group_set,
    get_group_by_name,
    create_group,
    get_number_of_groups_in_a_realm,
    create_subgroup,
)

from CheckmarxPythonSDK.CxOne.KeycloakAPI.dto import (
    GroupRepresentation
)

realm = "asean_2021_08"


def test_get_group_hierarchy():
    groups = get_group_hierarchy(realm=realm)
    assert groups is not None


def test_create_group_set():
    # ToDo
    """

    Returns:

    """
    # create_group_set()
    pass


def test_get_group_by_name():
    group_name = "CSM-Group"
    group = get_group_by_name(realm=realm, group_name=group_name)
    assert group is not None


def test_create_group():
    group_name = "happy-test-Group-2022-12-09"
    result = create_group(realm=realm, group_name=group_name)
    assert result is not None


def test_get_number_of_groups_in_a_realm():
    num = get_number_of_groups_in_a_realm(realm=realm)
    assert num > 0


def test_create_subgroup():
    group_name = "happy-test-Group-2022-12-09"
    group = get_group_by_name(realm=realm, group_name=group_name)
    group_id = group.id
    subgroup_name = "happy-test-Group-2022-12-09-subgroup"
    result = create_subgroup(realm=realm, group_id=group_id, subgroup_name=subgroup_name)
    assert result is True


def test_add_group_role():
    add_group_role()
