import importlib.util
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parent.parent
spec = importlib.util.spec_from_file_location(
    "release_changelog", ROOT / "scripts" / "release_changelog.py"
)
rc = importlib.util.module_from_spec(spec)
spec.loader.exec_module(rc)

BASE = (
    "# Changelog\nAll notable changes to this project will be documented in  this file.\n\n"
    "1.0.0 - 2026-01-01\n* [Add] old\n"
)


def test_fragments_are_ordered_by_tag_and_file_name():
    out = rc.build_release(
        BASE,
        {"b.md": "* [Fix] fix b\n", "a.md": "* [Add] add a\n* [Fix] fix a\n",
         "c.md": "* [Breaking] brk\n"},
        "1.1.0", "2026-02-02",
    )
    new, _, old = out.partition("1.0.0 - ")
    assert new.endswith("1.1.0 - 2026-02-02\n* [Breaking] brk\n* [Add] add a\n"
                        "* [Fix] fix a\n* [Fix] fix b\n\n")
    assert old.startswith("2026-01-01\n* [Add] old")


def test_legacy_unreleased_block_is_folded_in():
    legacy = BASE.replace("1.0.0 - 2026-01-01\n",
                          "Unreleased\n* [Fix] legacy\n\n1.0.0 - 2026-01-01\n")
    out = rc.build_release(legacy, {"a.md": "* [Add] new\n"}, "1.1.0", "2026-02-02")
    assert "Unreleased" not in out
    assert "1.1.0 - 2026-02-02\n* [Add] new\n* [Fix] legacy\n\n1.0.0" in out


def test_nothing_to_release_and_duplicate_version_fail():
    with pytest.raises(ValueError):
        rc.build_release(BASE, {}, "1.1.0", "2026-02-02")
    with pytest.raises(ValueError):
        rc.build_release(BASE, {"a.md": "* [Add] x\n"}, "1.0.0", "2026-02-02")


def test_cli_writes_changelog_and_removes_fragments(tmp_path):
    (tmp_path / "changelog.d").mkdir()
    (tmp_path / "CHANGELOG.md").write_text(BASE)
    (tmp_path / "changelog.d" / "README.md").write_text("docs")
    (tmp_path / "changelog.d" / "x.md").write_text("* [Add] x\n")
    assert rc.main(["1.1.0", "--date", "2026-02-02", "--root", str(tmp_path)]) == 0
    assert "1.1.0 - 2026-02-02\n* [Add] x\n" in (tmp_path / "CHANGELOG.md").read_text()
    assert not (tmp_path / "changelog.d" / "x.md").exists()
    assert (tmp_path / "changelog.d" / "README.md").exists()
