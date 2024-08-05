from CheckmarxPythonSDK.CxOne import (
    get_presets,
    create_new_preset,
    get_queries,
    get_preset_by_id,
    update_a_preset,
    delete_a_preset_by_id,
    get_preset_summary_by_id,
    clone_preset,
    add_query_to_preset,
)


def test_get_presets():
    result = get_presets()
    assert result is not None

    result = get_presets(include_details=True)
    assert result is not None


def test_create_new_preset():
    result = create_new_preset(name="happy_20240805_preset", description="test", query_ids=['14326086725136145656',
                                                                                            '12718155890111213901'])
    assert result is not None


def test_get_queries():
    result = get_queries()
    assert result is not None


def test_get_preset_by_id():
    result = get_preset_by_id(preset_id=107686231)
    assert result is not None


def test_update_a_preset():
    result = update_a_preset(preset_id=107686231, name="happy_test_20240805_preset")
    assert result is not None
    result = update_a_preset(preset_id=107686231,  name="happy_test_20240805_preset", description="happy test 20240805")
    assert result is not None
    result = update_a_preset(preset_id=107686231,  name="happy_test_20240805_preset", query_ids=['14326086725136145656'])
    assert result is not None


def test_delete_a_preset_by_id():
    pass


def test_get_preset_summary_by_id():
    result = get_preset_summary_by_id(preset_id=107686231)
    assert result is not None


def test_clone_preset():
    result = clone_preset(preset_id=107686231, name="happy_clone_test_preset", description="happy preset")
    assert result is not None


def test_add_query_to_preset():
    # HTTP 500
    result = add_query_to_preset(preset_id=1293655052, query_path="queries/Java/Java_High_Risk/Sql_injection/Sql_Injection.cs")
    assert result is not None
