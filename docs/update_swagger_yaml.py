#!/usr/bin/env python3
"""Update CxOne Swagger YAML files from the spec server.

The index at https://sng.ast.checkmarx.net/spec/v1? used to be a plain
directory listing of .yaml/.YAML links. It is now a Swagger UI page whose
spec list is embedded as a JSON `urls: [...]` array inside swagger-starter.js
(each entry is `{"name": ..., "url": "/spec/v1/<remote-name>.yaml"}`).
This crawls that page, downloads each referenced spec, and saves it to
swagger_yaml/CxOne/ (next to this script). Existing files are only
overwritten when the remote content differs.
"""

import hashlib
import http.client
import json
import os
import re
import sys
from typing import List, Optional
from urllib.request import Request, urlopen
from urllib.error import URLError
import logging
logger = logging.getLogger(__name__)

BASE_URL = "https://sng.ast.checkmarx.net/spec/v1"
OUTPUT_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "swagger_yaml", "CxOne")


def fetch_page(url: str) -> str:
    req = Request(url, headers={"User-Agent": "CxOne-Swagger-Updater/1.0"})
    with urlopen(req, timeout=30) as resp:
        return resp.read().decode("utf-8", errors="replace")


def extract_yaml_links(html: str) -> List[str]:
    """Extract .yaml/.YAML links referenced by the spec server's index page.

    Tries, in order:
      1. The legacy directory-listing forms (<a href="...">, markdown links).
      2. The current Swagger UI form: a `urls: [...]` JSON array embedded in
         swagger-starter.js, with each entry shaped like
         {"name": "...", "url": "/spec/v1/<remote-name>.yaml"}.
    """
    links: List[str] = []

    # <a href="..."> pattern (HTML directory listing)
    for m in re.finditer(r"""href\s*=\s*["']([^"']+\.(?:yaml|YAML))["']""", html):
        links.append(m.group(1))

    # [text](path) pattern (markdown rendering)
    for m in re.finditer(r"\[[^\]]*\]\(([^)]+\.(?:yaml|YAML))\)", html):
        links.append(m.group(1))

    if not links:
        links.extend(extract_yaml_links_from_swagger_ui(html))

    # Deduplicate while preserving order
    seen: set = set()
    result: List[str] = []
    for link in links:
        if link not in seen:
            seen.add(link)
            result.append(link)
    return result


def extract_yaml_links_from_swagger_ui(html: str) -> List[str]:
    """Extract spec URLs from a Swagger UI index page.

    The index page itself has no links -- it just loads swagger-starter.js,
    which calls SwaggerUIBundle with a `urls: [...]` option listing every
    spec. Fetch that script and pull the JSON array out of it.
    """
    script_match = re.search(r'src\s*=\s*["\']([^"\']*swagger-starter\.js)["\']', html)
    script_url = script_match.group(1) if script_match else "./swagger-starter.js"
    if script_url.startswith("http"):
        full_script_url = script_url
    elif script_url.startswith("/"):
        full_script_url = re.sub(r"(https?://[^/]+).*", r"\1", BASE_URL) + script_url
    else:
        full_script_url = BASE_URL + "/" + script_url.lstrip("./")

    try:
        script = fetch_page(full_script_url)
    except URLError as e:
        logger.error("  could not fetch {}: {}".format(full_script_url, e))
        return []

    urls_match = re.search(r"urls\s*:\s*(\[.*?\])\s*,\s*\n\s*oauth2RedirectUrl", script, re.DOTALL)
    if not urls_match:
        return []

    try:
        entries = json.loads(urls_match.group(1))
    except json.JSONDecodeError as e:
        logger.error("  could not parse spec list from {}: {}".format(full_script_url, e))
        return []

    links: List[str] = []
    for entry in entries:
        url = entry.get("url", "")
        if url.lower().endswith((".yaml", ".yml")):
            links.append(url)
    return links


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
    logger.info("Fetching file list from {}?...".format(BASE_URL))
    try:
        html = fetch_page(BASE_URL + "?")
    except URLError as e:
        logger.error("ERROR: could not fetch index page: {}".format(e))
        sys.exit(1)

    links = extract_yaml_links(html)
    logger.info("Found {} unique .yaml/.YAML links.".format(len(links)))

    updated = 0
    added = 0
    skipped = 0
    errors = 0

    for link in sorted(links):
        name = local_filename(link)
        filepath = os.path.join(OUTPUT_DIR, name)

        if link.startswith("http"):
            url = link
        elif link.startswith("/"):
            # Absolute path on the spec server's own host.
            host_match = re.match(r"(https?://[^/]+)", BASE_URL)
            url = host_match.group(1) + link
        else:
            url = BASE_URL + "/" + link

        try:
            req = Request(url, headers={"User-Agent": "CxOne-Swagger-Updater/1.0"})
            with urlopen(req, timeout=60) as resp:
                content = resp.read()

            if os.path.exists(filepath):
                old_hash = file_md5(filepath)
                new_hash = hashlib.md5(content).hexdigest()
                if old_hash == new_hash:
                    logger.info("  {:50s}  unchanged".format(name))
                    skipped += 1
                    continue
                logger.info("  {:50s}  updated".format(name))
                updated += 1
            else:
                logger.info("  {:50s}  new file".format(name))
                added += 1

            with open(filepath, "wb") as f:
                f.write(content)

        except (URLError, ValueError, http.client.InvalidURL) as e:
            # ValueError/InvalidURL cover malformed URLs (e.g. an unescaped
            # space in a remote filename) -- one bad entry in the spec
            # server's own index shouldn't abort the whole run.
            logger.error("  {:50s}  ERROR: {}".format(name, e))
            errors += 1

    logger.error("\nDone.  updated: {}  added: {}  skipped: {}  errors: {}".format(
        updated, added, skipped, errors))


if __name__ == "__main__":
    main()
