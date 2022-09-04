from CheckmarxPythonSDK.CxAST import (
    get_health_of_the_database,
    get_health_of_the_in_memory_db,
    get_health_of_the_message_queue,
    get_health_of_the_object_stroe_including_all_buckets,
    get_health_of_the_logging,
    get_health_of_the_scan_flow,
    get_health_of_the_sast_engines,
)


def test_get_health_of_the_database():
    health_check = get_health_of_the_database()
    assert health_check is not None


def test_get_health_of_the_in_memory_db():
    health_check = get_health_of_the_in_memory_db()
    assert health_check is not None


def test_get_health_of_the_message_queue():
    health_check = get_health_of_the_message_queue()
    assert health_check is not None


def test_get_health_of_the_object_stroe_including_all_buckets():
    health_check = get_health_of_the_object_stroe_including_all_buckets()
    assert health_check is not None


def test_get_health_of_the_logging():
    health_check = get_health_of_the_logging()
    assert health_check is not None


def test_get_health_of_the_scan_flow():
    health_check = get_health_of_the_scan_flow()
    assert health_check is not None


def test_get_health_of_the_sast_engines():
    health_check = get_health_of_the_sast_engines()
    assert health_check is not None
