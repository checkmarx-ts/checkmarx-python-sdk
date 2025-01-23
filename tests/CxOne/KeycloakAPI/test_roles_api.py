from CheckmarxPythonSDK.CxOne.KeycloakAPI import (
    get_all_roles_for_the_client,
    create_a_role_for_the_client,
    get_a_role_by_name,
    update_a_role_by_id,
    get_roles_children,
    create_a_composite_role_children,
)

from CheckmarxPythonSDK.CxOne.KeycloakAPI.dto import (
    UserRepresentation
)

realm = "happy"


def test_get_all_roles_for_the_client():
    roles = get_all_roles_for_the_client(realm=realm, client_id="d3b60524-13a1-431a-a703-1d6d3d09f512")
    assert roles is not None

