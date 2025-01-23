from CheckmarxPythonSDK.CxOne.KeycloakAPI import (
    get_all_oauth_clients,
    get_oauth_client_by_name,
    get_all_oauth_client_by_id,
    create_oauth_client,
    edit_auth_client,
    get_oauth_service_account_user,
    add_group_to_oauth_client,
    generate_oauth_secret,
    get_client_ast_app,
)


def test_get_client_ast_app():
    client_ast_app = get_client_ast_app(realm="happy")
    assert client_ast_app is not None
