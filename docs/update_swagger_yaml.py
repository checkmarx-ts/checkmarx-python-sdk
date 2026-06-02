#!/usr/bin/env python3
"""Update CxOne Swagger YAML files from the spec server.

Crawls https://sng.ast.checkmarx.net/spec/v1? for .yaml/.YAML links,
downloads them, and saves to this directory. Existing files are only
overwritten when the remote content differs.
"""

import hashlib
import os
import re
import sys
from typing import List, Optional
from urllib.request import Request, urlopen
from urllib.error import URLError

BASE_URL = "https://sng.ast.checkmarx.net/spec/v1"
OUTPUT_DIR = os.path.dirname(os.path.abspath(__file__))


def fetch_page(url: str) -> str:
    req = Request(url, headers={"User-Agent": "CxOne-Swagger-Updater/1.0"})
    with urlopen(req, timeout=30) as resp:
        return resp.read().decode("utf-8", errors="replace")


def extract_yaml_links(html: str) -> List[str]:
    """Extract .yaml/.YAML hrefs from the directory-listing page."""
    links: List[str] = []

    # <a href="..."> pattern (HTML directory listing)
    for m in re.finditer(r"""href\s*=\s*["']([^"']+\.(?:yaml|YAML))["']""", html):
        links.append(m.group(1))

    # [text](path) pattern (markdown rendering)
    for m in re.finditer(r"\[[^\]]*\]\(([^)]+\.(?:yaml|YAML))\)", html):
        links.append(m.group(1))

    # Deduplicate while preserving order
    seen: set = set()
    result: List[str] = []
    for link in links:
        if link not in seen:
            seen.add(link)
            result.append(link)
    return result


def local_filename(remote_path: str) -> str:
    """Derive local filename from a remote path.

    Remote names follow the pattern:
      singapore-{kebab-path}-{UPPER_NAME}.yaml
    We take the last hyphen-separated segment as the local name.
    """
    name = os.path.basename(remote_path)
    if "-" in name:
        name = name.rsplit("-", 1)[-1]
    return name


def file_md5(path: str) -> Optional[str]:
    if not os.path.exists(path):
        return None
    h = hashlib.md5()
    with open(path, "rb") as f:
        for chunk in iter(lambda: f.read(65536), b""):
            h.update(chunk)
    return h.hexdigest()


def main() -> None:
    print("Fetching file list from {}?...".format(BASE_URL))
    try:
        html = fetch_page(BASE_URL + "?")
    except URLError as e:
        print("ERROR: could not fetch index page: {}".format(e), file=sys.stderr)
        sys.exit(1)

    links = extract_yaml_links(html)
    print("Found {} unique .yaml/.YAML links.".format(len(links)))

    updated = 0
    added = 0
    skipped = 0
    errors = 0

    for link in sorted(links):
        name = local_filename(link)
        filepath = os.path.join(OUTPUT_DIR, name)

        url = link if link.startswith("http") else BASE_URL + "/" + link

        try:
            req = Request(url, headers={"User-Agent": "CxOne-Swagger-Updater/1.0"})
            with urlopen(req, timeout=60) as resp:
                content = resp.read()

            if os.path.exists(filepath):
                old_hash = file_md5(filepath)
                new_hash = hashlib.md5(content).hexdigest()
                if old_hash == new_hash:
                    print("  {:50s}  unchanged".format(name))
                    skipped += 1
                    continue
                print("  {:50s}  updated".format(name))
                updated += 1
            else:
                print("  {:50s}  new file".format(name))
                added += 1

            with open(filepath, "wb") as f:
                f.write(content)

        except URLError as e:
            print("  {:50s}  ERROR: {}".format(name, e), file=sys.stderr)
            errors += 1

    print("\nDone.  updated: {}  added: {}  skipped: {}  errors: {}".format(
        updated, added, skipped, errors))


if __name__ == "__main__":
    main()
