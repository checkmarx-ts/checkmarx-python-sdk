#!/usr/bin/env python3
"""Fold changelog.d/*.md fragments into CHANGELOG.md for a release.

Usage: python scripts/release_changelog.py VERSION [--date YYYY-MM-DD] [--dry-run]
"""
import argparse
import datetime
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
TAG_ORDER = ["Breaking", "Change", "Add", "Fix", "Document"]
HEADER_END = "this file.\n\n"  # end of the fixed intro in CHANGELOG.md


def _tag_rank(line: str) -> int:
    m = re.match(r"\*\s*\[(\w+)\]", line)
    tag = m.group(1) if m else None
    return TAG_ORDER.index(tag) if tag in TAG_ORDER else len(TAG_ORDER)


def _bullets(text: str) -> list:
    return [ln.rstrip() for ln in text.splitlines() if ln.strip()]


def build_release(changelog: str, fragments: dict, version: str, date: str) -> str:
    """Return the new CHANGELOG text.

    fragments: {file name: text}. A legacy "Unreleased" block, if present,
    is folded in too.
    """
    if f"\n{version} - " in changelog:
        raise ValueError(f"version {version} already in the changelog")
    head, sep, rest = changelog.partition(HEADER_END)
    if not sep:
        raise ValueError("unexpected CHANGELOG.md header")
    lines = []
    if rest.startswith("Unreleased\n"):
        block, _, rest = rest.partition("\n\n")
        lines += _bullets(block[len("Unreleased\n"):])
        rest = rest.lstrip("\n")
    for name in sorted(fragments):
        lines += _bullets(fragments[name])
    if not lines:
        raise ValueError("nothing to release: no fragments and no Unreleased entries")
    lines.sort(key=_tag_rank)  # stable: keeps file order within a tag
    section = f"{version} - {date}\n" + "\n".join(lines) + "\n\n"
    return head + sep + section + rest


def main(argv=None) -> int:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("version")
    ap.add_argument("--date", default=datetime.date.today().isoformat())
    ap.add_argument("--dry-run", action="store_true")
    ap.add_argument("--root", type=Path, default=ROOT)
    args = ap.parse_args(argv)

    changelog_path = args.root / "CHANGELOG.md"
    files = sorted(
        p for p in (args.root / "changelog.d").glob("*.md") if p.name != "README.md"
    )
    fragments = {p.name: p.read_text(encoding="utf-8") for p in files}
    new = build_release(
        changelog_path.read_text(encoding="utf-8"), fragments, args.version, args.date
    )
    if args.dry_run:
        sys.stdout.write(new[:3000])
        return 0
    changelog_path.write_text(new, encoding="utf-8")
    for p in files:
        p.unlink()
    print(f"CHANGELOG.md updated for {args.version}; removed {len(files)} fragment(s)")
    return 0


if __name__ == "__main__":
    sys.exit(main())
