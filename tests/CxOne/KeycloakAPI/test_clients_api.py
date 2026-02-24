from CheckmarxPythonSDK.CxOne.KeycloakAPI import (
    ClientsApi,
)
from pprint import pprint

def test_get_client_ast_app():
    clients = ClientsApi().get_clients(realm="happy")
    print(f"number of clients: {len(clients)}")
    for client in clients:
        pprint(client)
    assert clients is not None
