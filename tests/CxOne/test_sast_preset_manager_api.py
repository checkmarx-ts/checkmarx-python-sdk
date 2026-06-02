import pytest

from CheckmarxPythonSDK.CxOne import (
    get_sast_presets,
    get_sast_preset_by_id,
    create_sast_preset,
    delete_sast_preset,
    clone_sast_preset,
    get_sast_query_families,
    get_sast_queries_by_family,
)


SCANNER = "sast"


def test_get_sast_presets():
    result = get_sast_presets(scanner=SCANNER, limit=5)
    assert result is not None
    assert "presets" in result


def test_get_sast_preset_by_id():
    presets = get_sast_presets(scanner=SCANNER, limit=1)
    preset_list = presets.get("presets", [])
    if not preset_list:
        pytest.skip("No presets found")
    preset_id = preset_list[0].get("id")
    result = get_sast_preset_by_id(scanner=SCANNER, id=preset_id)
    assert result is not None
    assert "queries" in result


def test_get_sast_query_families():
    result = get_sast_query_families(scanner=SCANNER)
    assert result is not None
    assert isinstance(result, list)


def test_get_sast_queries_by_family():
    families = get_sast_query_families(scanner=SCANNER)
    if not families:
        pytest.skip("No query families found")
    result = get_sast_queries_by_family(
        scanner=SCANNER, query_family=families[0]
    )
    assert result is not None
    assert isinstance(result, list)


def test_create_and_delete_sast_preset():
    families = get_sast_query_families(scanner=SCANNER)
    if not families:
        pytest.skip("No query families found")

    queries = get_sast_queries_by_family(
        scanner=SCANNER, query_family=families[0]
    )
    query_ids = []
    def collect_ids(items):
        for item in items:
            if item.get("isLeaf") and item.get("data"):
                qid = item["data"].get("queryDescriptionId")
                if qid:
                    query_ids.append(qid)
            if item.get("children"):
                collect_ids(item["children"])
    collect_ids(queries)
    if not query_ids:
        pytest.skip("No query IDs available")

    qid = str(query_ids[0])
    preset_name = "test-sdk-preset"

    # Clean up old test preset
    existing = get_sast_presets(scanner=SCANNER, search_term=preset_name,
                                   exact_match=True, limit=10)
    for p in existing.get("presets", []):
        if p.get("name") == preset_name:
            try:
                delete_sast_preset(scanner=SCANNER, id=p["id"])
            except Exception:
                pass

    # Create
    created = create_sast_preset(
        scanner=SCANNER,
        name=preset_name,
        description="SDK test preset",
        queries=[{
            "familyName": families[0],
            "totalCount": 1,
            "queryIds": [qid],
        }],
    )
    assert created is not None
    preset_id = created.get("id")
    assert preset_id is not None

    # Delete
    is_deleted = delete_sast_preset(scanner=SCANNER, id=preset_id)
    assert is_deleted is True


def test_clone_sast_preset():
    presets = get_sast_presets(scanner=SCANNER, limit=1)
    preset_list = presets.get("presets", [])
    if not preset_list:
        pytest.skip("No presets found")

    preset_id = preset_list[0].get("id")
    clone_name = "test-sdk-clone-{}".format(
        __import__("datetime").datetime.now().strftime("%H%M%S")
    )
    cloned = clone_sast_preset(
        scanner=SCANNER, id=preset_id, name=clone_name
    )
    assert cloned is not None
    assert "id" in cloned

    # Cleanup
    delete_sast_preset(scanner=SCANNER, id=cloned["id"])
