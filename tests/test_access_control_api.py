

from CheckmarxPythonSDK.CxRestAPISDK import AccessControlAPI


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
    resp = ac.get_all_ldap_role_mapping()
    assert resp is not None


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
    permission_id = 1
    ac = AccessControlAPI()
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


def test_create_new_role():
    ac = AccessControlAPI()
    name = "commonAuditor"
    description = "a auditor with scanner, auditor, verifier"
    permission_ids = [4, 6, 7, 8]
    resp = ac.create_new_role(name=name, description=description, permission_ids=permission_ids)
    assert resp is True


def test_get_role_by_id():
    role_id = 1
    ac = AccessControlAPI()
    resp = ac.get_role_by_id(role_id)
    assert resp is not None


def test_update_a_role():
    ac = AccessControlAPI()
    role_id = 1004
    name = "auditorCommon"
    description = "common auditor"
    permission_ids = [4, 6, 7, 8]

    resp = ac.update_a_role(role_id=role_id, name=name, description=description, permission_ids=permission_ids)
    assert resp is True


def test_delete_a_role():
    ac = AccessControlAPI()
    role_id = 1004
    resp = ac.delete_a_role(role_id=role_id)
    assert resp is True


def test_get_all_saml_identity_providers():
    ac = AccessControlAPI()
    all_saml_identity_providers = ac.get_all_saml_identity_providers()
    assert all_saml_identity_providers is not None


def test_create_new_saml_identity_provider():
    ac = AccessControlAPI()

    certificate_file_path = \
        r"C:\Users\HappyY\Documents\Checkmarx\CxSAST\Integration\SAML Integration\SAML Integration CER Files\test.cer"
    active = "true"
    name = "CxSAML"
    issuer = "test1"
    login_url = 'https://srvl.idpname.com/app/checkmarxdev/sso/saml'
    logout_url = None
    error_url = None
    sign_authn_request = "true"
    authn_request_binding = "HTTP-Redirect"
    is_manual_management = "true"
    default_team_id = "4"
    default_role_id = "1021"

    is_successful = ac.create_new_saml_identity_provider(
        certificate_file_path=certificate_file_path, active=active, name=name, issuer=issuer, login_url=login_url,
        logout_url=logout_url, error_url=error_url, sign_authn_request=sign_authn_request,
        authn_request_binding=authn_request_binding, is_manual_management=is_manual_management,
        default_team_id=default_team_id, default_role_id=default_role_id
    )
    assert is_successful is True


def test_get_saml_identity_provider_by_id():
    ac = AccessControlAPI()


def test_update_new_saml_identity_provider():
    ac = AccessControlAPI()
    # update_new_saml_identity_provider(self, saml_identity_provider_id, certificate_file, active, name, issuer,
    #                                   login_url, logout_url, error_url, sign_authn_request, authn_request_binding,
    #                                   is_manual_management, default_team_id, default_role_id)


def test_delete_a_saml_identity_provider():
    ac = AccessControlAPI()


def test_get_details_of_saml_role_mappings():
    ac = AccessControlAPI()
    saml_role_mapping = ac.get_details_of_saml_role_mappings(saml_identity_provider_id=1)
    assert saml_role_mapping is not None


def test_set_saml_group_and_role_mapping_details():
    ac = AccessControlAPI()
    sample_role_mapping_details = [
              {
                "roleName": "SAST Scanner",
                "samlAttributeValue": "IT"
              }
            ]
    is_successful = ac.set_saml_group_and_role_mapping_details(
        saml_identity_provider_id=1,
        sample_role_mapping_details=sample_role_mapping_details
    )
    assert is_successful is True

def test_get_saml_service_provider_metadata():
    ac = AccessControlAPI()
    saml_service_provider_metadata = ac.get_saml_service_provider_metadata()

    assert saml_service_provider_metadata is not None


def test_get_saml_service_provider():
    ac = AccessControlAPI()
    saml_service_provider = ac.get_saml_service_provider()
    assert saml_service_provider is not None


def test_update_a_saml_service_provider():
    ac = AccessControlAPI()
    certificate_file_path = ""
    certificate_password = ""
    issuer = ""
    is_successful = ac.update_a_saml_service_provider(certificate_file_path, certificate_password, issuer)
    assert is_successful is True


def test_get_details_of_saml_team_mappings():
    ac = AccessControlAPI()
    saml_team_mapping = ac.get_details_of_saml_team_mappings(saml_identity_provider_id=1)
    assert saml_team_mapping is not None


def test_set_saml_group_and_team_mapping_details():
    ac = AccessControlAPI()
    saml_team_mapping_details = [
         {
            "teamFullPath": "/CxServer/CompanyOne/AC_TEAM_ONE",
            "samlAttributeValue": "IT"
         },
         {
            "teamFullPath": "/CxServer/CompanyOne/AC_TEAM_TWO",
            "samlAttributeValue": "Sales"
         },
         {
            "teamFullPath": "/CxServer/CompanyTwo/AC_Dev_Team",
            "samlAttributeValue": "IT"
         }
        ]
    is_successful = ac.set_saml_group_and_team_mapping_details(
        saml_identity_provider_id=1, saml_team_mapping_details=saml_team_mapping_details
    )
    assert is_successful is True

def test_get_all_service_providers():
    ac = AccessControlAPI()
    resp = ac.get_all_service_providers()
    assert resp is not None


def test_get_service_provider_by_id():
    ac = AccessControlAPI()
    service_provider_id = 1
    resp = ac.get_service_provider_by_id(service_provider_id=service_provider_id)
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
    smtp_settings_id = 2
    resp = ac.get_smtp_settings_by_id(smtp_settings_id=smtp_settings_id)
    assert resp is not None


def test_update_smtp_settings():
    ac = AccessControlAPI()
    smtp_settings_id = 2
    host = "***"
    port = 25
    encryption_type = "None"
    from_address = "***"
    use_default_credentials = "false"
    username = "***"
    password = "***"
    resp = ac.update_smtp_settings(smtp_settings_id, password, host, port, encryption_type, from_address,
                                   use_default_credentials, username)
    assert resp is True


def test_delete_smtp_settings():
    ac = AccessControlAPI()
    smtp_settings_id = 1
    resp = ac.delete_smtp_settings(smtp_settings_id=smtp_settings_id)
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


def test_get_members_by_team_id():
    ac = AccessControlAPI()
    team_id = ac.get_team_id_by_full_name("/CxServer")
    resp = ac.get_members_by_team_id(team_id=team_id)
    assert resp is not None


def test_update_members_by_team_id():
    ac = AccessControlAPI()

    team_id = ac.get_team_id_by_full_name("/CxServer")
    user_ids = [1008, 1007]
    is_successful = ac.update_members_by_team_id(team_id=team_id, user_ids=user_ids)
    assert is_successful is True


def test_add_a_user_to_a_team():
    ac = AccessControlAPI()
    team_id = ac.get_team_id_by_full_name("/CxServer")

    user_id = 7

    is_successful = ac.add_a_user_to_a_team(team_id=team_id, user_id=user_id)

    assert is_successful is True


def test_delete_a_member_from_a_team():
    ac = AccessControlAPI()
    team_id = ac.get_team_id_by_full_name("/CxServer")
    user_id = 7

    is_successful = ac.delete_a_member_from_a_team(team_id=team_id, user_id=user_id)
    assert is_successful is True


def test_get_all_teams():
    ac = AccessControlAPI()
    resp = ac.get_all_teams()
    assert resp is not None


def test_get_team_id_by_full_name():
    ac = AccessControlAPI()
    team_id = ac.get_team_id_by_full_name("/CxServer")
    assert team_id is not None


def test_create_new_team():
    ac = AccessControlAPI()

    parent_team_full_name = "/CxServer"
    team_name = "avengers_team"
    team_id = ac.get_team_id_by_full_name(full_name=parent_team_full_name + "/" + team_name)
    parent_id = ac.get_team_id_by_full_name(full_name=parent_team_full_name)

    if not team_id and parent_id:
        is_successful = ac.create_new_team(name=team_name, parent_id=parent_id)
        assert is_successful is True


def test_get_team_by_id():
    ac = AccessControlAPI()

    team_id = ac.get_team_id_by_full_name("/CxServer")

    team = ac.get_team_by_id(team_id=team_id)

    assert team is not None


def test_update_a_team():
    ac = AccessControlAPI()

    parent_team_full_name = "/CxServer"
    team_name = "avengers_team"
    team_id = ac.get_team_id_by_full_name(full_name=parent_team_full_name + "/" + team_name)
    parent_id = ac.get_team_id_by_full_name(full_name=parent_team_full_name)

    is_successful = ac.update_a_team(team_id=team_id, name=team_name, parent_id=parent_id)

    assert is_successful is True


def test_delete_a_team():
    ac = AccessControlAPI()

    parent_team_full_name = "/CxServer"
    team_name = "avengers_team"
    team_id = ac.get_team_id_by_full_name(full_name=parent_team_full_name + "/" + team_name)

    is_successful = ac.delete_a_team(team_id=team_id)

    assert is_successful is True


def test_generate_a_new_token_signing_certificate():
    ac = AccessControlAPI()

    is_successful = ac.generate_a_new_token_signing_certificate()

    assert is_successful is True


def test_upload_a_new_token_signing_certificate():
    ac = AccessControlAPI()
    # TODO


def test_get_all_users():
    ac = AccessControlAPI()

    all_users = ac.get_all_users()

    assert len(all_users) > 1


def test_get_user_id_by_name():
    ac = AccessControlAPI()

    username = "test3"

    user_id = ac.get_user_id_by_name(username=username)

    assert user_id is not None


def test_create_new_user():
    ac = AccessControlAPI()

    username = 'test3'
    password = 'Password01!'
    role_ids = None
    team_ids = [1022]
    authentication_provider_id = 1
    first_name = 'test'
    last_name = 'test'
    email = 'test3@test.com'
    phone_number = None
    cell_phone_number = None
    job_title = None
    other = None
    country = None
    active = 'true'
    expiration_date = '2023-04-28'
    allowed_ip_list = None
    locale_id = 1

    is_successful = ac.create_new_user(username=username, password=password, role_ids=role_ids, team_ids=team_ids,
                                       authentication_provider_id=authentication_provider_id, first_name=first_name,
                                       last_name=last_name, email=email, phone_number=phone_number,
                                       cell_phone_number=cell_phone_number,
                                       job_title=job_title, other=other, country=country, active=active,
                                       expiration_date=expiration_date, allowed_ip_list=allowed_ip_list,
                                       locale_id=locale_id)

    assert is_successful is True


def test_get_user_by_id():
    ac = AccessControlAPI()

    username = "test"
    user_id = ac.get_user_id_by_name(username=username)

    user = ac.get_user_by_id(user_id=user_id)

    assert user is not None


def test_update_a_user():
    ac = AccessControlAPI()

    username = "test3"
    user_id = ac.get_user_id_by_name(username=username)

    role_ids = [3]
    team_ids = [1022]
    first_name = "Bruce"
    last_name = "Lee"
    email = "test3@test.cn"
    phone_number = None
    cell_phone_number = None
    job_title = None
    other = None
    country = None
    active = "false"
    expiration_date = "2020-07-30 12:00:00"
    allowed_ip_list = None
    locale_id = 1

    is_successful = ac.update_a_user(user_id=user_id, role_ids=role_ids, team_ids=team_ids, first_name=first_name,
                                     last_name=last_name, email=email, phone_number=phone_number,
                                     cell_phone_number=cell_phone_number, job_title=job_title, other=other,
                                     country=country, active=active, expiration_date=expiration_date,
                                     allowed_ip_list=allowed_ip_list, locale_id=locale_id)

    assert is_successful is True


def test_delete_a_user():
    ac = AccessControlAPI()

    username = "test3"
    user_id = ac.get_user_id_by_name(username=username)

    is_successful = ac.delete_a_user(user_id=user_id)

    assert is_successful is True


# def test_migrate_existing_user():
#     ac = AccessControlAPI()
#
#     creation_date
#     username
#     password
#     role_ids
#     team_ids
#     authentication_provider_id
#     first_name
#     last_name
#     email
#     phone_number
#     cell_phone_number
#     job_title
#     other
#     country
#     active
#     expiration_date
#     allowed_ip_list
#     locale_id
#     is_successful = ac.migrate_existing_user(creation_date, username, password, role_ids, team_ids,
#     authentication_provider_id,
#                           first_name, last_name, email, phone_number, cell_phone_number, job_title, other, country,
#                           active, expiration_date, allowed_ip_list, locale_id)


def test_get_all_windows_domains():
    ac = AccessControlAPI()

    all_windows_domains = ac.get_all_windows_domains()

    assert len(all_windows_domains) >= 1


def test_get_windows_domain_id_by_name():
    ac = AccessControlAPI()

    name = "test"

    windows_domain_id = ac.get_windows_domain_id_by_name(name=name)

    assert windows_domain_id is not None


def test_create_a_new_windows_domain():
    ac = AccessControlAPI()

    windows_domain_name = "test_domain"
    full_qualified_name = "dd.local"

    is_successful = ac.create_a_new_windows_domain(name=windows_domain_name, full_qualified_name=full_qualified_name)

    assert is_successful is True


def test_get_windows_domain_by_id():
    ac = AccessControlAPI()
    name = "test"

    windows_domain_id = ac.get_windows_domain_id_by_name(name=name)
    windows_domain = ac.get_windows_domain_by_id(windows_domain_id)
    assert windows_domain is not None


def test_update_a_windows_domain():
    ac = AccessControlAPI()

    name = "test"

    windows_domain_id = ac.get_windows_domain_id_by_name(name=name)
    full_qualified_name = "test2222.local"
    is_successful = ac.update_a_windows_domain(windows_domain_id, name, full_qualified_name)

    assert is_successful is True


def test_delete_a_windows_domain():
    ac = AccessControlAPI()
    name = "test"

    windows_domain_id = ac.get_windows_domain_id_by_name(name=name)
    is_successful = ac.delete_a_windows_domain(windows_domain_id=windows_domain_id)
    assert is_successful is True

