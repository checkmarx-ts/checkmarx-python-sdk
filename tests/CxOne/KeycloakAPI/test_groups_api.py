from CheckmarxPythonSDK.CxOne.KeycloakAPI import (

    get_group_hierarchy,
    create_group_set,
    get_group_by_name,
    get_number_of_groups_in_a_realm,
    get_group_by_id,
    update_group_by_id,
    delete_group_by_id,
    create_subgroup,
    get_group_permissions,
    update_group_permissions,
    get_group_members,
    create_group,

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


def test_get_group_by_id():
    # "CSM-Group"
    group_id = '36e79d6f-ce11-4a5c-91d3-53a3661e76f4'
    group = get_group_by_id(realm=realm, group_id=group_id)
    assert group is not None


def test_update_group_by_id():
    # TODO
    # "CSM-Group"
    group_id = '36e79d6f-ce11-4a5c-91d3-53a3661e76f4'
    group_representation = None
    # group_representation = GroupRepresentation(
    #     access, attributes, client_roles, group_representation_id, name, path, realm_roles, sub_groups
    # )
    result = update_group_by_id(realm=realm, group_id=group_id, group_representation=group_representation)
    assert result is True


def test_delete_group_by_id():
    # happy-test-Group-2022-12-09
    group_id = '726c4029-e8ab-4c13-a904-31c907fba666'
    result = delete_group_by_id(realm=realm, group_id=group_id)
    assert result is True


def test_create_subgroup():
    group_name = "happy-test-Group-2022-12-09"
    group = get_group_by_name(realm=realm, group_name=group_name)
    group_id = group.id
    subgroup_name = "happy-test-Group-2022-12-09-subgroup"
    result = create_subgroup(realm=realm, group_id=group_id, subgroup_name=subgroup_name)
    assert result is True


def test_get_group_permissions():
    # "CSM-Group"
    group_id = '36e79d6f-ce11-4a5c-91d3-53a3661e76f4'
    permissions = get_group_permissions(realm=realm, group_id=group_id)
    assert permissions is not None


def test_update_group_permissions():
    # "CSM-Group"
    group_id = '36e79d6f-ce11-4a5c-91d3-53a3661e76f4'
    # TODO
    update_group_permissions


def test_get_group_members():
    group_id = '15c87c0f-ab8c-4fc1-aec9-124b23c2b014'
    result = get_group_members(realm=realm, group_id=group_id)
    assert result is not None



# def test_add_group_role():
#     add_group_role()
