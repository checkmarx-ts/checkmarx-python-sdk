from CheckmarxPythonSDK.CxAST import (
    create_an_application,
    get_a_list_of_applications,
    get_application_id_by_name,
    get_all_application_tags,
    get_an_application_by_id,
    update_an_application,
    delete_an_application,
    create_an_application_rule,
    get_a_list_of_rules_for_a_specific_application,
    get_an_application_rule,
    update_an_application_rule,
    delete_an_application_rule,
)

application_name = "happy-test-application-2022-03-02"


def test_create_an_application():
    application = create_an_application(name=application_name)
    assert application is not None


def test_get_a_list_of_applications():
    response = get_a_list_of_applications()
    applications = response.get("applications")
    assert len(applications) > 1


def test_get_application_id_by_name():
    application_id = get_application_id_by_name(name=application_name)
    assert application_id is not None


def test_get_all_application_tags():
    all_tags = get_all_application_tags()
    assert all_tags is not None


def test_get_an_application_by_id():
    application = get_an_application_by_id(application_id='8b5cafa7-44fe-4dff-a713-8344f021fdd1')
    assert application is not None


def test_update_an_application():
    is_successful = update_an_application(application_id='8b5cafa7-44fe-4dff-a713-8344f021fdd1',
                                          description="test description")
    assert is_successful is True


def test_create_an_application_rule():
    application_id = get_application_id_by_name(name=application_name)
    rule_type = "project.name.contains"
    rule_value = "happy"
    application_rule = create_an_application_rule(application_id, rule_type, rule_value)
    assert application_rule is not None


def test_get_a_list_of_rules_for_a_specific_application():
    application_id = get_application_id_by_name(name=application_name)
    application_rules = get_a_list_of_rules_for_a_specific_application(application_id=application_id)
    assert application_rules is not None


def test_get_an_application_rule():
    application_id = get_application_id_by_name(name=application_name)
    application_rules = get_a_list_of_rules_for_a_specific_application(application_id=application_id)
    if application_rules:
        rule_id = application_rules[-1].get("id")
        application_rule = get_an_application_rule(application_id=application_id, rule_id=rule_id)
        assert application_rule is not None


def test_update_an_application_rule():
    application_id = get_application_id_by_name(name=application_name)
    application_rules = get_a_list_of_rules_for_a_specific_application(application_id=application_id)
    if application_rules:
        rule_id = application_rules[0].get("id")
        application_rule = update_an_application_rule(application_id=application_id, rule_id=rule_id,
                                                      rule_type="project.name.contains", rule_value="happy")
        assert application_rule is True


def test_delete_an_application_rule():
    application_id = get_application_id_by_name(name=application_name)
    application_rules = get_a_list_of_rules_for_a_specific_application(application_id=application_id)
    if application_rules:
        rule_id = application_rules[0].get("id")
        is_successful = delete_an_application_rule(application_id=application_id, rule_id=rule_id)
        assert is_successful is True


def test_delete_an_application():
    application_id = get_application_id_by_name(name=application_name)
    is_successful = delete_an_application(application_id=application_id)
    assert is_successful is True
