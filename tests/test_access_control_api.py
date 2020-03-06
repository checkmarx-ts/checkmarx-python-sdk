

from CheckmarxPythonSDK.CxRestAPISDK.accesscontrol.AccessControlAPI import AccessControlAPI


def test_get_all_assignable_users():
    ac = AccessControlAPI()
    resp = ac.get_all_assignable_users()
    assert resp is not None
    if list(resp):
        user = resp[0]
        assert user.id == 1


def test_get_all_authentication_providers():
    ac = AccessControlAPI()
    resp = ac.get_all_authentication_providers()
    assert resp is not None
    if list(resp):
        provider = resp[0]
        assert provider.id == 1


def test_submit_first_admin_user():
    ac = AccessControlAPI()
    resp = ac.submit_first_admin_user("dd", "Password01!", "Alex", "Smith", "alex.smith@test.com")
    assert resp is not None


def test_get_admin_user_exists_confirmation():
    ac = AccessControlAPI()
    resp = ac.get_admin_user_exists_confirmation()
    assert resp is True


def test_get_all_ldap_role_mapping():
    ac = AccessControlAPI()


def test_get_my_profile():
    ac = AccessControlAPI()
    resp = ac.get_my_profile()
    assert resp is not None


def test_update_my_profile():
    ac = AccessControlAPI()
    first_name = "test"
    last_name = "test"
    email = "test@test.com"
    phone_number = "153"
    cell_phone_number = "2332"
    job_title = "something"
    other = ""
    country = "China"
    locale_id = 7
    resp = ac.update_my_profile(first_name=first_name, last_name=last_name, email=email, phone_number=phone_number,
                                cell_phone_number=cell_phone_number, job_title=job_title, other=other, country=country,
                                locale_id=locale_id)
    assert resp is True


def test_get_all_permissions():
    ac = AccessControlAPI()
    resp = ac.get_all_permissions()
    assert resp is not None


def test_get_permission_by_id():
    id = 1
    ac = AccessControlAPI()
    resp = ac.get_permission_by_id(id)
    assert resp is not None


def test_get_all_roles():
    ac = AccessControlAPI()
    resp = ac.get_all_roles()
    assert resp is not None


def test_create_new_role():
    ac = AccessControlAPI()
    name = "commonAuditor"
    description = "a auditor with scanner, auditor, verifier"
    permission_ids = [4, 6, 7, 8]
    resp = ac.create_new_role(name=name, description=description, permission_ids=permission_ids)
    assert resp is True


def test_get_role_by_id():
    id = 1
    ac = AccessControlAPI()
    resp = ac.get_role_by_id(id)
    assert resp is not None


def test_update_a_role():
    ac = AccessControlAPI()
    id = 1004
    name = "auditorCommon"
    description = "common auditor"
    permission_ids = [4, 6, 7, 8]

    resp = ac.update_a_role(id=id, name=name, description=description, permission_ids=permission_ids)
    assert resp is True


def test_delete_a_role():
    ac = AccessControlAPI()
    id = 1004
    resp = ac.delete_a_role(id=id)
    assert resp is True


def test_get_all_service_providers():
    ac = AccessControlAPI()
    resp = ac.get_all_service_providers()
    assert resp is not None


def test_get_service_provider_by_id():
    ac = AccessControlAPI()
    id = 1
    resp = ac.get_service_provider_by_id(id)
    assert resp is not None


def test_get_all_smtp_settings():
    ac = AccessControlAPI()
    resp = ac.get_all_smtp_settings()
    assert resp is not None


def test_create_smtp_settings():
    ac = AccessControlAPI()
    host = "***"
    port = 25
    encryption_type = "None"
    from_address = "***"
    use_default_credentials = "false"
    username = "***"
    password = "***"
    resp = ac.create_smtp_settings(password, host, port, encryption_type, from_address, use_default_credentials,
                                   username)

    assert resp is True


def test_get_smtp_settings_by_id():
    ac = AccessControlAPI()
    id = 2
    resp = ac.get_smtp_settings_by_id(id=id)
    assert resp is not None


def test_update_smtp_settings():
    ac = AccessControlAPI()
    id = 2
    host = "***"
    port = 25
    encryption_type = "None"
    from_address = "***"
    use_default_credentials = "false"
    username = "***"
    password = "***"
    resp = ac.update_smtp_settings(id, password, host, port, encryption_type, from_address, use_default_credentials,
                                   username)
    assert resp is True


def test_delete_smtp_settings():
    ac = AccessControlAPI()
    id = 1
    resp = ac.delete_smtp_settings(id=id)
    assert resp is True


def test_test_smtp_connection():
    ac = AccessControlAPI()
    receiver_email = "***"
    host = "***"
    port = 25
    encryption_type = "None"
    from_address = "***"
    use_default_credentials = "false"
    username = "***"
    password = "***"
    resp = ac.test_smtp_connection(receiver_email=receiver_email, password=password, host=host, port=port,
                                   encryption_type=encryption_type, from_address=from_address,
                                   use_default_credentials=use_default_credentials, username=username)
    assert resp is True


def test_get_all_system_locales():
    ac = AccessControlAPI()
    resp = ac.get_all_system_locales()
    assert resp is not None
