from CheckmarxPythonSDK.CxOne import (
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

from CheckmarxPythonSDK.CxOne.dto import (
    ApplicationInput,
    RuleInput,
)

application_name = "happy-test-application-2025-09-08"


def test_create_an_application():
    application_id = get_application_id_by_name(name=application_name)
    if application_id:
        return
    application_input = ApplicationInput(
        name=application_name,
        rules=[
            RuleInput(
                type="project.name.contains",
                value="test"
            )
        ],
        tags={
            "test": "",
            "priority": "high"
        }
    )
    application = create_an_application(application_input=application_input)
    assert application is not None


def test_get_a_list_of_applications():
    app_collection = get_a_list_of_applications()
    applications = app_collection.applications
    assert len(applications) >= 1


def test_get_a_list_of_applications_with_tags_keys():
    app_collection = get_a_list_of_applications(tags_keys=["test"])
    applications = app_collection.applications
    assert len(applications) >= 1


def test_get_a_list_of_applications_with_tags_values():
    app_collection = get_a_list_of_applications(tags_values=["high"])
    applications = app_collection.applications
    assert len(applications) == 1


def test_get_application_id_by_name():
    application_id = get_application_id_by_name(name=application_name)
    assert application_id is not None


def test_get_all_application_tags():
    all_tags = get_all_application_tags()
    assert all_tags is not None


def test_get_an_application_by_id():
    application_id = get_application_id_by_name(name=application_name)
    application = get_an_application_by_id(application_id=application_id)
    assert application is not None


def test_update_an_application():
    application_id = get_application_id_by_name(name=application_name)

    application_input = ApplicationInput(
        name=application_name,
        description="happy test 2022-03-08",
        rules=[
            RuleInput(
                type="project.name.contains",
                value="test"
            )
        ],
        tags={
            "test": "",
            "priority": "high"
        }
    )

    is_successful = update_an_application(application_id=application_id,
                                          application_input=application_input)
    assert is_successful is True


def test_create_an_application_rule():
    application_id = get_application_id_by_name(name=application_name)
    rule_input = RuleInput(
        type="project.name.contains",
        value="happy"
    )
    application_rule = create_an_application_rule(application_id, rule_input=rule_input)
    assert application_rule is not None


def test_get_a_list_of_rules_for_a_specific_application():
    application_id = get_application_id_by_name(name=application_name)
    application_rules = get_a_list_of_rules_for_a_specific_application(application_id=application_id)
    assert application_rules is not None


def test_get_an_application_rule():
    application_id = get_application_id_by_name(name=application_name)
    application_rules = get_a_list_of_rules_for_a_specific_application(application_id=application_id)
    if application_rules:
        rule_id = application_rules[-1].id
        application_rule = get_an_application_rule(application_id=application_id, rule_id=rule_id)
        assert application_rule is not None


def test_update_an_application_rule():
    application_id = get_application_id_by_name(name=application_name)
    application_rules = get_a_list_of_rules_for_a_specific_application(application_id=application_id)
    if application_rules:
        rule_id = application_rules[-1].id
        rule_input = RuleInput(
            type="project.name.contains",
            value="happy1"
        )
        application_rule = update_an_application_rule(
            application_id=application_id, rule_id=rule_id, rule_input=rule_input
        )
        assert application_rule is True


def test_delete_an_application_rule():
    application_id = get_application_id_by_name(name=application_name)
    application_rules = get_a_list_of_rules_for_a_specific_application(application_id=application_id)
    if application_rules:
        rule_id = application_rules[0].id
        is_successful = delete_an_application_rule(application_id=application_id, rule_id=rule_id)
        assert is_successful is True


def test_delete_an_application():
    application_id = get_application_id_by_name(name=application_name)
    is_successful = delete_an_application(application_id=application_id)
    assert is_successful is True
