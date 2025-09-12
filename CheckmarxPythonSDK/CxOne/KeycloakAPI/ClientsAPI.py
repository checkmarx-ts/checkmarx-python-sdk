import json
from CheckmarxPythonSDK.api_client import ApiClient
from CheckmarxPythonSDK.CxOne.config import construct_configuration
from CheckmarxPythonSDK.CxOne.KeycloakAPI.url import api_url
import time
from requests import Response


class ClientsAPI(object):

    def __init__(self, api_client: ApiClient = None):
        if api_client is None:
            configuration = construct_configuration()
            api_client = ApiClient(configuration=configuration)
        self.api_client = api_client

    def get_all_oauth_clients(self, realm: str) -> Response:
        relative_url = api_url + f"/{realm}/clients?first=0&max=999999&search=True"
        response = self.api_client.get_request(relative_url=relative_url, is_iam=True)
        return response

    def get_oauth_client_by_name(self, realm: str, client_name: str) -> Response:
        relative_url = api_url + f"/{realm}/clients?first=0&max=999999&search=True"
        response = self.api_client.get_request(relative_url=relative_url, is_iam=True)

        for client in response.json():
            if client_name == client['clientId']:
                response = client
        return response

    def get_all_oauth_client_by_id(self, realm: str, client_id: str) -> Response:
        relative_url = api_url + f"/{realm}/clients/{client_id}"
        response = self.api_client.get_request(relative_url=relative_url, is_iam=True)
        return response

    def create_oauth_client(self, realm: str, client_name: str) -> Response:
        relative_url = api_url + f"/{realm}/clients"
        post_data = json.dumps(
            {
                'enabled': True,
                'attributes': {},
                'redirectUris': [],
                'clientId': client_name,
                'protocol': 'openid-connect'
            }
        )
        response = self.api_client.post_request(relative_url=relative_url, data=post_data, is_iam=True)
        return response

    def edit_auth_client(self, realm: str, client_id: str, client_name: str, name: str, description: str) -> Response:
        relative_url = api_url + f"/{realm}/clients/{client_id}"
        current_time = int(time.time())
        put_data = json.dumps(
            {
                "id": client_id,
                "clientId": client_name,
                "name": name,
                "description": description,
                "surrogateAuthRequired": False,
                "enabled": True,
                "alwaysDisplayInConsole": False,
                "clientAuthenticatorType": "client-secret",
                "redirectUris": [],
                "webOrigins": [],
                "notBefore": 0,
                "bearerOnly": False,
                "consentRequired": False,
                "standardFlowEnabled": False,
                "implicitFlowEnabled": False,
                "directAccessGrantsEnabled": True,
                "serviceAccountsEnabled": True,
                "publicClient": False,
                "frontchannelLogout": True,
                "protocol": "openid-connect",
                "attributes": {
                    "client.secret.creation.time": current_time,
                    "backchannel.logout.session.required": "true",
                    "backchannel.logout.revoke.offline.tokens": "false",
                    "lastUpdate": current_time
                },
                "authenticationFlowBindingOverrides": {},
                "fullScopeAllowed": True,
                "nodeReRegistrationTimeout": -1,
                "protocolMappers": [
                    {
                        "name": "Client IP Address",
                        "protocol": "openid-connect",
                        "protocolMapper": "oidc-usersessionmodel-note-mapper",
                        "consentRequired": False,
                        "config": {
                            "user.session.note": "clientAddress",
                            "id.token.claim": "True",
                            "access.token.claim": "True",
                            "claim.name": "clientAddress",
                            "jsonType.label": "String"
                        }
                    },
                    {
                        "name": "Client ID",
                        "protocol": "openid-connect",
                        "protocolMapper": "oidc-usersessionmodel-note-mapper",
                        "consentRequired": False,
                        "config": {
                            "user.session.note": "clientId",
                            "id.token.claim": "True",
                            "access.token.claim": "True",
                            "claim.name": "clientId",
                            "jsonType.label": "String"
                        }
                    },
                    {
                        "name": "Client Host",
                        "protocol": "openid-connect",
                        "protocolMapper": "oidc-usersessionmodel-note-mapper",
                        "consentRequired": False,
                        "config": {
                            "user.session.note": "clientHost",
                            "id.token.claim": "True",
                            "access.token.claim": "True",
                            "claim.name": "clientHost",
                            "jsonType.label": "String"
                        }
                    }
                ],
                "defaultClientScopes": [
                    "web-origins",
                    "acr",
                    "roles",
                    "profile",
                    "iam-api",
                    "groups",
                    "ast-api",
                    "email"
                ],
                "optionalClientScopes": [
                    "address",
                    "phone",
                    "offline_access",
                    "microprofile-jwt"
                ],
                "access": {
                    "view": True,
                    "configure": True,
                    "manage": True
                },
            }
        )
        response = self.api_client.put_request(relative_url=relative_url, data=put_data, is_iam=True)
        return response

    def get_oauth_service_account_user(self, realm: str, client_id: str) -> dict:
        relative_url = api_url + f"/{realm}/clients/{client_id}/service-account-user"
        response = self.api_client.get_request(relative_url=relative_url, is_iam=True)
        return response.json()

    def add_group_to_oauth_client(self, realm: str, service_account_user_id: str, group_id: str) -> Response:
        relative_url = api_url + f"/{realm}/users/{service_account_user_id}/groups/{group_id}"
        put_data = json.dumps(
            {
                "realm": f"{realm}",
                "userId": f"{service_account_user_id}",
                "groupId": f"{group_id}"
            }
        )
        response = self.api_client.put_request(relative_url=relative_url, data=put_data, is_iam=True)
        return response

    def generate_oauth_secret(self, realm: str, client_id: str) -> Response:
        relative_url = api_url + f"/{realm}/clients/{client_id}/client-secret"
        post_data = json.dumps(
            {
                "realm": realm,
                "client": client_id
            }
        )
        response = self.api_client.post_request(relative_url=relative_url, data=post_data, is_iam=True)
        return response

    def get_client_ast_app(self, realm: str) -> dict:
        """

        Args:
            realm:

        Returns:

            example

            [
                {
                    "id": "d3b60524-13a1-431a-a703-1d6d3d09f512",
                    "clientId": "ast-app",
                    "rootUrl": "https://sng.iam.checkmarx.net",
                    "adminUrl": "https://sng.iam.checkmarx.net/*",
                    "surrogateAuthRequired": false,
                    "enabled": true,
                    "alwaysDisplayInConsole": false,
                    "clientAuthenticatorType": "client-secret",
                    "redirectUris": [
                        "https://sng.ast.checkmarx.net/*",
                        "/*"
                    ],
                    "webOrigins": [
                        "*",
                        "/*"
                    ],
                    "notBefore": 0,
                    "bearerOnly": false,
                    "consentRequired": false,
                    "standardFlowEnabled": true,
                    "implicitFlowEnabled": true,
                    "directAccessGrantsEnabled": true,
                    "serviceAccountsEnabled": true,
                    "publicClient": true,
                    "frontchannelLogout": true,
                    "protocol": "openid-connect",
                    "attributes": {
                        "saml.assertion.signature": "false",
                        "security.admin.console": "true",
                        "saml.force.post.binding": "false",
                        "saml.multivalued.roles": "false",
                        "saml.encrypt": "false",
                        "post.logout.redirect.uris": "+",
                        "saml.server.signature": "false",
                        "saml.server.signature.keyinfo.ext": "false",
                        "exclude.session.state.from.auth.response": "false",
                        "saml_force_name_id_format": "false",
                        "saml.client.signature": "false",
                        "tls.client.certificate.bound.access.tokens": "false",
                        "saml.authnstatement": "false",
                        "display.on.consent.screen": "false",
                        "secretExpDaysBeforeNotification": "10",
                        "saml.onetimeuse.condition": "false"
                    },
                    "authenticationFlowBindingOverrides": {},
                    "fullScopeAllowed": true,
                    "nodeReRegistrationTimeout": -1,
                    "protocolMappers": [
                        {
                            "id": "76fcd170-9b8b-4991-8e69-38d9fdf80619",
                            "name": "realm-management client roles",
                            "protocol": "openid-connect",
                            "protocolMapper": "oidc-usermodel-client-role-mapper",
                            "consentRequired": false,
                            "config": {
                                "multivalued": "true",
                                "user.attribute": "foo",
                                "access.token.claim": "true",
                                "claim.name": "resource_access.${client_id}.roles",
                                "jsonType.label": "String",
                                "usermodel.clientRoleMapping.clientId": "realm-management"
                            }
                        },
                        {
                            "id": "b359cb2c-ac34-428d-b7d9-8bd8453926a6",
                            "name": "Client ID",
                            "protocol": "openid-connect",
                            "protocolMapper": "oidc-usersessionmodel-note-mapper",
                            "consentRequired": false,
                            "config": {
                                "user.session.note": "clientId",
                                "userinfo.token.claim": "true",
                                "id.token.claim": "true",
                                "access.token.claim": "true",
                                "claim.name": "clientId",
                                "jsonType.label": "String"
                            }
                        },
                        {
                            "id": "aad7d17c-d733-4ed3-8c14-e11590a9678d",
                            "name": "Client IP Address",
                            "protocol": "openid-connect",
                            "protocolMapper": "oidc-usersessionmodel-note-mapper",
                            "consentRequired": false,
                            "config": {
                                "user.session.note": "clientAddress",
                                "userinfo.token.claim": "true",
                                "id.token.claim": "true",
                                "access.token.claim": "true",
                                "claim.name": "clientAddress",
                                "jsonType.label": "String"
                            }
                        },
                        {
                            "id": "470d9673-888e-4f6f-9f4a-1b6fd652c099",
                            "name": "Client Host",
                            "protocol": "openid-connect",
                            "protocolMapper": "oidc-usersessionmodel-note-mapper",
                            "consentRequired": false,
                            "config": {
                                "user.session.note": "clientHost",
                                "userinfo.token.claim": "true",
                                "id.token.claim": "true",
                                "access.token.claim": "true",
                                "claim.name": "clientHost",
                                "jsonType.label": "String"
                            }
                        }
                    ],
                    "defaultClientScopes": [
                        "web-origins",
                        "roles",
                        "profile",
                        "iam-api",
                        "groups",
                        "basic",
                        "ast-api",
                        "email"
                    ],
                    "optionalClientScopes": [
                        "address",
                        "phone",
                        "microprofile-jwt"
                    ],
                    "access": {
                        "view": true,
                        "configure": true,
                        "manage": true
                    }
                }
            ]
        """
        relative_url = api_url + f"/{realm}/clients?clientId=ast-app&max=1&search=true"
        response = self.api_client.get_request(relative_url=relative_url, is_iam=True)
        response = response.json()
        return response


def get_all_oauth_clients(realm: str) -> Response:
    return ClientsAPI().get_all_oauth_clients(realm=realm)


def get_oauth_client_by_name(realm: str, client_name: str) -> Response:
    return ClientsAPI().get_oauth_client_by_name(realm=realm, client_name=client_name)


def get_all_oauth_client_by_id(realm: str, client_id: str) -> Response:
    return ClientsAPI().get_all_oauth_client_by_id(realm=realm, client_id=client_id)


def create_oauth_client(realm: str, client_name: str) -> Response:
    return ClientsAPI().create_oauth_client(realm=realm, client_name=client_name)


def edit_auth_client(realm: str, client_id: str, client_name: str, name: str, description: str) -> Response:
    return ClientsAPI().edit_auth_client(realm=realm, client_id=client_id, client_name=client_name, name=name,
                                         description=description)


def get_oauth_service_account_user(realm: str, client_id: str) -> dict:
    return ClientsAPI().get_oauth_service_account_user(realm=realm, client_id=client_id)


def add_group_to_oauth_client(realm: str, service_account_user_id: str, group_id: str) -> Response:
    return ClientsAPI().add_group_to_oauth_client(realm=realm, service_account_user_id=service_account_user_id,
                                                  group_id=group_id)


def generate_oauth_secret(realm: str, client_id: str) -> Response:
    return ClientsAPI().generate_oauth_secret(realm=realm, client_id=client_id)


def get_client_ast_app(realm: str) -> dict:
    return ClientsAPI().get_client_ast_app(realm=realm)
