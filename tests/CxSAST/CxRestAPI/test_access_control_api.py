import pytest
from CheckmarxPythonSDK.CxRestAPISDK import AccessControlAPI
from CheckmarxPythonSDK.utilities.CxError import BadRequestError

_TEST_ROLE_NAME = "pytest_tmp_role"
_TEST_TEAM_NAME = "avengers_team"
_TEST_USERNAME = "pytest_tmp_user3"


def test_get_all_assignable_users():
    ac = AccessControlAPI()
    resp = ac.get_all_assignable_users()
    assert len(resp) > 0


def test_get_all_authentication_providers():
    ac = AccessControlAPI()
    resp = ac.get_all_authentication_providers()
    assert len(resp) > 0


def test_submit_first_admin_user():
    ac = AccessControlAPI()
    with pytest.raises((BadRequestError, ValueError)):
        ac.submit_first_admin_user("dd", "DummyPassword0#*)", "Alex", "Smith", "alex.smith@test.com")


def test_get_admin_user_exists_confirmation():
    ac = AccessControlAPI()
    resp = ac.get_admin_user_exists_confirmation()
    assert resp is True


def test_get_all_ldap_role_mapping():
    ac = AccessControlAPI()
    resp = ac.get_all_ldap_role_mapping()
    assert resp is not None


def test_get_my_profile():
    ac = AccessControlAPI()
    resp = ac.get_my_profile()
    assert resp.username is not None


@pytest.mark.skip(reason="update_my_profile requires current password confirmation not supported by the SDK API signature")
def test_update_my_profile():
    pass


def test_get_all_oidc_clients():
    ac = AccessControlAPI()
    oidc_clients = ac.get_all_oidc_clients()
    assert len(oidc_clients) > 0


def test_get_all_permissions():
    ac = AccessControlAPI()
    resp = ac.get_all_permissions()
    assert resp is not None


def test_get_permission_by_id():
    ac = AccessControlAPI()
    permissions = ac.get_all_permissions()
    assert permissions is not None and len(permissions) > 0
    permission_id = permissions[0].id
    resp = ac.get_permission_by_id(permission_id)
    assert resp is not None


def test_get_all_roles():
    ac = AccessControlAPI()
    resp = ac.get_all_roles()
    assert resp is not None


def test_get_role_id_by_name():
    ac = AccessControlAPI()
    resp = ac.get_role_id_by_name("Admin")
    assert isinstance(resp, int)

    resp = ac.get_role_id_by_name(["Admin", "SAST Admin"])
    assert isinstance(resp, list)


def test_create_update_delete_role():
    ac = AccessControlAPI()
    existing_id = ac.get_role_id_by_name(_TEST_ROLE_NAME)
    if existing_id:
        ac.delete_a_role(role_id=existing_id)

    permission_ids = [4, 6, 7, 8]
    resp = ac.create_new_role(
        name=_TEST_ROLE_NAME,
        description="a auditor with scanner, auditor, verifier",
        permission_ids=permission_ids,
    )
    assert resp is True

    role_id = ac.get_role_id_by_name(_TEST_ROLE_NAME)
    assert role_id is not None

    resp = ac.update_a_role(
        role_id=role_id,
        name=_TEST_ROLE_NAME,
        description="updated auditor",
        permission_ids=permission_ids,
    )
    assert resp is True

    resp = ac.delete_a_role(role_id=role_id)
    assert resp is True


def test_get_role_by_id():
    ac = AccessControlAPI()
    role_id = ac.get_role_id_by_name("Admin")
    assert role_id is not None
    resp = ac.get_role_by_id(role_id)
    assert resp is not None


def test_get_all_saml_identity_providers():
    ac = AccessControlAPI()
    all_saml_identity_providers = ac.get_all_saml_identity_providers()
    assert all_saml_identity_providers is not None


@pytest.mark.skip(reason="Requires a SAML certificate file not available in CI")
def test_create_new_saml_identity_provider():
    pass


def test_get_saml_identity_provider_by_id():
    pass


def test_update_new_saml_identity_provider():
    pass


def test_delete_a_saml_identity_provider():
    pass


def test_get_details_of_saml_role_mappings():
    ac = AccessControlAPI()
    providers = ac.get_all_saml_identity_providers()
    if not providers:
        pytest.skip("No SAML identity providers configured")
    saml_role_mapping = ac.get_details_of_saml_role_mappings(saml_identity_provider_id=providers[0].id)
    assert saml_role_mapping is not None


def test_get_saml_service_provider_metadata():
    ac = AccessControlAPI()
    saml_service_provider_metadata = ac.get_saml_service_provider_metadata()
    assert saml_service_provider_metadata is not None


def test_get_saml_service_provider():
    ac = AccessControlAPI()
    saml_service_provider = ac.get_saml_service_provider()
    assert saml_service_provider is not None


def test_get_details_of_saml_team_mappings():
    ac = AccessControlAPI()
    providers = ac.get_all_saml_identity_providers()
    if not providers:
        pytest.skip("No SAML identity providers configured")
    saml_team_mapping = ac.get_details_of_saml_team_mappings(saml_identity_provider_id=providers[0].id)
    assert saml_team_mapping is not None


def test_get_all_service_providers():
    ac = AccessControlAPI()
    resp = ac.get_all_service_providers()
    assert resp is not None


def test_get_service_provider_by_id():
    ac = AccessControlAPI()
    providers = ac.get_all_service_providers()
    if not providers:
        pytest.skip("No service providers available")
    resp = ac.get_service_provider_by_id(service_provider_id=providers[0].id)
    assert resp is not None


def test_get_all_smtp_settings():
    ac = AccessControlAPI()
    resp = ac.get_all_smtp_settings()
    assert resp is not None


@pytest.mark.skip(reason="Requires a real SMTP server")
def test_create_smtp_settings():
    pass


@pytest.mark.skip(reason="Requires a pre-existing SMTP settings entry")
def test_get_smtp_settings_by_id():
    pass


@pytest.mark.skip(reason="Requires a pre-existing SMTP settings entry")
def test_update_smtp_settings():
    pass


@pytest.mark.skip(reason="Requires a pre-existing SMTP settings entry")
def test_delete_smtp_settings():
    pass


@pytest.mark.skip(reason="Requires a real SMTP server")
def test_test_smtp_connection():
    pass


def test_get_all_system_locales():
    ac = AccessControlAPI()
    resp = ac.get_all_system_locales()
    assert resp is not None


def test_get_members_by_team_id():
    ac = AccessControlAPI()
    team_id = ac.get_team_id_by_full_name("/CxServer")
    resp = ac.get_members_by_team_id(team_id=team_id)
    assert resp is not None


def test_update_members_by_team_id():
    ac = AccessControlAPI()
    team_id = ac.get_team_id_by_full_name("/CxServer")
    all_users = ac.get_all_users()
    # Keep all existing users (don't remove any to avoid breaking manage-users constraint)
    user_ids = [u.id for u in all_users]
    is_successful = ac.update_members_by_team_id(team_id=team_id, user_ids=user_ids)
    assert is_successful is True


def test_add_and_delete_user_from_team():
    ac = AccessControlAPI()
    root_team_id = ac.get_team_id_by_full_name("/CxServer")
    auth_providers = ac.get_all_authentication_providers()
    auth_provider_id = auth_providers[0].id if auth_providers else 1

    # Create a child team so the temp user always has at least one team
    child_team_name = "pytest_child_team"
    child_team_full = f"/CxServer/pytest_child_team"
    child_team_id = ac.get_team_id_by_full_name(child_team_full)
    if not child_team_id:
        ac.create_new_team(name=child_team_name, parent_id=root_team_id)
        child_team_id = ac.get_team_id_by_full_name(child_team_full)

    tmp_user = "_pytest_tmp_team_member"
    existing_id = ac.get_user_id_by_name(tmp_user)
    if existing_id:
        ac.delete_a_user(user_id=existing_id)

    ac.create_new_user(
        username=tmp_user, password="Password01!",
        role_ids=None, team_ids=[child_team_id],
        authentication_provider_id=auth_provider_id,
        first_name="tmp", last_name="tmp",
        email=f"{tmp_user}@test.com",
        active="true", expiration_date="2099-12-31",
        phone_number=None, cell_phone_number=None, job_title=None,
        other=None, country=None, allowed_ip_list=None, locale_id=1,
    )
    user_id = ac.get_user_id_by_name(tmp_user)
    assert user_id is not None

    # Add to root team, then remove (user still has child_team as backup)
    is_successful = ac.add_a_user_to_a_team(team_id=root_team_id, user_id=user_id)
    assert is_successful is True

    is_successful = ac.delete_a_member_from_a_team(team_id=root_team_id, user_id=user_id)
    assert is_successful is True

    ac.delete_a_user(user_id=user_id)
    if child_team_id:
        ac.delete_a_team(team_id=child_team_id)


def test_get_all_teams():
    ac = AccessControlAPI()
    resp = ac.get_all_teams()
    assert resp is not None


def test_get_team_id_by_full_name():
    ac = AccessControlAPI()
    team_id = ac.get_team_id_by_full_name("/CxServer")
    assert team_id is not None


def test_create_and_delete_team():
    ac = AccessControlAPI()
    parent_team_full_name = "/CxServer"
    parent_id = ac.get_team_id_by_full_name(full_name=parent_team_full_name)
    team_id = ac.get_team_id_by_full_name(full_name=f"{parent_team_full_name}/{_TEST_TEAM_NAME}")

    if not team_id and parent_id:
        is_successful = ac.create_new_team(name=_TEST_TEAM_NAME, parent_id=parent_id)
        assert is_successful is True

    team_id = ac.get_team_id_by_full_name(full_name=f"{parent_team_full_name}/{_TEST_TEAM_NAME}")
    if team_id:
        is_successful = ac.delete_a_team(team_id=team_id)
        assert is_successful is True


def test_create_teams_recursively():
    ac = AccessControlAPI()
    team_full_name = "/CxServer/DevOps/Golden Team/Box"
    team_ids = ac.create_teams_recursively(team_full_name)
    # Returns newly created team IDs; may be empty if teams already exist
    assert team_ids is not None
    # Verify the full path now exists
    assert ac.get_team_id_by_full_name(team_full_name) is not None


def test_get_team_by_id():
    ac = AccessControlAPI()
    team_id = ac.get_team_id_by_full_name("/CxServer")
    team = ac.get_team_by_id(team_id=team_id)
    assert team is not None


def test_update_a_team():
    ac = AccessControlAPI()
    parent_team_full_name = "/CxServer"
    parent_id = ac.get_team_id_by_full_name(full_name=parent_team_full_name)
    team_id = ac.get_team_id_by_full_name(full_name=f"{parent_team_full_name}/{_TEST_TEAM_NAME}")
    if team_id is None:
        if parent_id:
            ac.create_new_team(name=_TEST_TEAM_NAME, parent_id=parent_id)
        team_id = ac.get_team_id_by_full_name(full_name=f"{parent_team_full_name}/{_TEST_TEAM_NAME}")
    if team_id is None:
        pytest.skip(f"Team '{_TEST_TEAM_NAME}' could not be found or created")
    is_successful = ac.update_a_team(team_id=team_id, name=_TEST_TEAM_NAME, parent_id=parent_id)
    assert is_successful is True


@pytest.mark.skip(reason="Rotating the signing certificate invalidates all active tokens mid-suite")
def test_generate_a_new_token_signing_certificate():
    ac = AccessControlAPI()
    is_successful = ac.generate_a_new_token_signing_certificate()
    assert is_successful is True


def test_upload_a_new_token_signing_certificate():
    pass


def test_get_all_users():
    ac = AccessControlAPI()
    all_users = ac.get_all_users()
    assert len(all_users) >= 1


def test_create_update_delete_user():
    ac = AccessControlAPI()
    auth_providers = ac.get_all_authentication_providers()
    auth_provider_id = auth_providers[0].id if auth_providers else 1
    team_id = ac.get_team_id_by_full_name("/CxServer")

    existing_id = ac.get_user_id_by_name(_TEST_USERNAME)
    if existing_id:
        ac.delete_a_user(user_id=existing_id)

    is_successful = ac.create_new_user(
        username=_TEST_USERNAME,
        password="Password01!",
        role_ids=None,
        team_ids=[team_id],
        authentication_provider_id=auth_provider_id,
        first_name="test",
        last_name="test",
        email=f"{_TEST_USERNAME}@test.com",
        phone_number=None,
        cell_phone_number=None,
        job_title=None,
        other=None,
        country=None,
        active="true",
        expiration_date="2099-12-31",
        allowed_ip_list=None,
        locale_id=1,
    )
    assert is_successful is True

    user_id = ac.get_user_id_by_name(_TEST_USERNAME)
    assert user_id is not None

    user = ac.get_user_by_id(user_id=user_id)
    assert user is not None

    is_successful = ac.update_a_user(
        user_id=user_id,
        role_ids=[3],
        team_ids=[team_id],
        first_name="Bruce",
        last_name="Lee",
        email=f"{_TEST_USERNAME}@test.cn",
        phone_number=None,
        cell_phone_number=None,
        job_title=None,
        other=None,
        country=None,
        active="false",
        expiration_date="2099-07-30 12:00:00",
        allowed_ip_list=None,
        locale_id=1,
    )
    assert is_successful is True

    is_successful = ac.delete_a_user(user_id=user_id)
    assert is_successful is True


def test_get_user_id_by_name():
    ac = AccessControlAPI()
    all_users = ac.get_all_users()
    if not all_users:
        pytest.skip("No users available")
    username = all_users[0].username
    user_id = ac.get_user_id_by_name(username=username)
    assert user_id is not None


def test_get_all_windows_domains():
    ac = AccessControlAPI()
    all_windows_domains = ac.get_all_windows_domains()
    assert len(all_windows_domains) >= 0


def test_create_update_delete_windows_domain():
    ac = AccessControlAPI()
    domain_name = "pytest_tmp_domain"
    fqdn = "pytest-tmp.local"

    existing_id = ac.get_windows_domain_id_by_name(domain_name)
    if existing_id:
        ac.delete_a_windows_domain(windows_domain_id=existing_id)

    is_successful = ac.create_a_new_windows_domain(name=domain_name, full_qualified_name=fqdn)
    assert is_successful is True

    domain_id = ac.get_windows_domain_id_by_name(domain_name)
    assert domain_id is not None

    domain = ac.get_windows_domain_by_id(domain_id)
    assert domain is not None

    is_successful = ac.update_a_windows_domain(domain_id, domain_name, "pytest-updated.local")
    assert is_successful is True

    is_successful = ac.delete_a_windows_domain(windows_domain_id=domain_id)
    assert is_successful is True


def test_get_windows_domain_id_by_name():
    ac = AccessControlAPI()
    all_domains = ac.get_all_windows_domains()
    if not all_domains:
        pytest.skip("No Windows domains configured")
    name = all_domains[0].name
    domain_id = ac.get_windows_domain_id_by_name(name=name)
    assert domain_id is not None
