#!/usr/bin/env python3
"""Generate docs/CxOne_REST_API_List.md from the Python SDK + Swagger YAML specs.

For every `def method_name(self, ...)` in a CxOne `*API.py` file that makes an
`api_client.call_api(method=..., url=...)` call, resolves the HTTP method and
endpoint path, then looks up which `docs/swagger_yaml/CxOne/*.yaml` file (if
any) documents that exact endpoint. Produces a
`| Swagger YAML | Python Class | Method | HTTP | Endpoint Path |` table,
one row per SDK method, grouped by source file.

Reuses the URL-resolution helpers from cross_reference_endpoints.py so the
two scripts never drift apart on how a Python `url = ...` expression maps to
an absolute path.
"""

import importlib.util
import os
import re
import sys
from typing import Dict, List, Optional, Tuple
import logging
logger = logging.getLogger(__name__)

SDK_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
CXONE_DIR = os.path.join(SDK_DIR, "CheckmarxPythonSDK", "CxOne")
YAML_DIR = os.path.join(SDK_DIR, "docs", "swagger_yaml", "CxOne")
OUTPUT_PATH = os.path.join(SDK_DIR, "docs", "CxOne_REST_API_List.md")

# Reuse extract_base_path / clean_url_expr / resolve_url / scan_yaml_files /
# simplify from the sibling script instead of re-implementing them.
_spec = importlib.util.spec_from_file_location(
    "cross_reference_endpoints", os.path.join(os.path.dirname(os.path.abspath(__file__)), "cross_reference_endpoints.py")
)
xref = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(xref)

EXCLUDE_FILES = {"scaAPI.py"}  # wraps the separate CxScaApiSDK package
KEYCLOAK_ROW = "| keycloak.yaml | (KeycloakAPI/\\*) | (multiple classes) | — | `/auth/admin/realms/*` |"


def resolve_url_with_base_path_attr(url_expr: str, base_path_attr_value: str) -> Optional[str]:
    """Resolve a `f"{self.base_url}{self._base_path}/suffix"`-style expression.

    Companion to xref.resolve_url() for the `_base_path`-class-attribute shape
    (see scan_python_api_methods()): `{self.base_url}` is the server root here
    (resolves to ""), and `{self._base_path}` is the class attribute's value.
    """
    expr = url_expr.strip()
    if not ((expr.startswith('f"') and expr.endswith('"')) or (expr.startswith("f'") and expr.endswith("'"))):
        return None
    inner = expr[2:-1]
    inner = inner.replace("{self.base_url}", "")
    inner = inner.replace("{self._base_path}", base_path_attr_value)
    inner = re.sub(r'/+', '/', inner)
    return inner


def scan_python_api_methods(fname: str, source: str) -> Tuple[Optional[str], List[Tuple[str, str, str]]]:
    """Return (class_name, [(method_name, http_method, resolved_path), ...]) in source order."""
    # Files commonly define DTO/helper classes before the actual API wrapper
    # class, so don't just take the first `class ...` -- every API wrapper
    # class in this SDK is named `*API`, so look for that specifically.
    api_class_matches = re.findall(r'^class\s+(\w+API)\b', source, re.MULTILINE)
    if api_class_matches:
        class_name = api_class_matches[-1]
    else:
        class_match = re.search(r'^class\s+(\w+)', source, re.MULTILINE)
        class_name = class_match.group(1) if class_match else None

    base_path = xref.extract_base_path(source)
    fallback_base_path: Optional[str] = None
    if base_path is None:
        # A few files (e.g. scaManagementOfRiskAPI.py, scaPrivateRegistryConfigAPI.py)
        # set `self.base_url = self.api_client.configuration.server_base_url` (no
        # path suffix) and build each URL from a separate `_base_path` class
        # attribute instead, e.g. f"{self.base_url}{self._base_path}/packages".
        # extract_base_path() doesn't recognize that shape, so fall back to it here.
        base_path_attr_match = re.search(r'_base_path\s*=\s*["\']([^"\']+)["\']', source)
        if base_path_attr_match and re.search(
            r'self\.base_url\s*=\s*self\.api_client\.configuration\.server_base_url', source
        ):
            fallback_base_path = base_path_attr_match.group(1).rstrip("/")
            base_path = ""  # {self.base_url} resolves to the server root in this shape
        else:
            return class_name, []

    lines = source.split("\n")
    n = len(lines)
    results: List[Tuple[str, str, str]] = []

    current_method_name: Optional[str] = None
    current_url_expr: Optional[str] = None
    found_for_current: bool = False

    def method_indent_level(line: str) -> int:
        return len(line) - len(line.lstrip(" "))

    i = 0
    while i < n:
        line = lines[i]

        # A new `def` at 4-space indent starts a new SDK method.
        def_match = re.match(r'( {4})def\s+(\w+)\s*\(', line)
        if def_match:
            current_method_name = def_match.group(2)
            current_url_expr = None
            found_for_current = False
            i += 1
            continue

        if current_method_name is None or current_method_name.startswith("_"):
            i += 1
            continue

        url_match = re.match(r'\s*url\s*=\s*(.+)', line)
        if url_match:
            raw = url_match.group(1).strip()
            if raw == "(":
                # `url = (` with the single, complete f-string on the next
                # line and nothing but the closing paren after that, e.g.:
                #   url = (
                #       f"{self.base_url}{self._base_path}/foo/bar"
                #   )
                # Some methods instead concatenate multiple string segments
                # across several lines (e.g. a bare f"{self.server_base_url}"
                # followed by a separate literal path segment) -- bail out on
                # those rather than resolve to just the first segment.
                if i + 2 < n and lines[i + 2].strip() == ")":
                    cleaned = xref.clean_url_expr(lines[i + 1].strip())
                    if cleaned:
                        current_url_expr = cleaned
            else:
                cleaned = xref.clean_url_expr(raw)
                if cleaned:
                    current_url_expr = cleaned

        meth_match = re.search(r'method\s*=\s*["\']([A-Z]+)["\']', line)
        if meth_match and not found_for_current:
            http_method = meth_match.group(1)
            url_expr = current_url_expr

            inline_url = re.search(
                r'url\s*=\s*((?:f"[^"]+"|f\'[^\']+\'|self\.base_url(?:\s*\+\s*["\'][^"\']+["\'])?))',
                line,
            )
            if inline_url:
                cleaned_inline = xref.clean_url_expr(inline_url.group(1))
                if cleaned_inline:
                    url_expr = cleaned_inline
            else:
                for j in range(i + 1, min(i + 3, n)):
                    next_line = lines[j]
                    if re.search(r'method\s*=\s*["\']', next_line):
                        break
                    nxt_url_match = re.match(r'\s*url\s*=\s*(.+)', next_line)
                    if nxt_url_match:
                        cleaned = xref.clean_url_expr(nxt_url_match.group(1))
                        if cleaned:
                            url_expr = cleaned
                        break

            if url_expr:
                if fallback_base_path is not None:
                    resolved = resolve_url_with_base_path_attr(url_expr, fallback_base_path)
                else:
                    resolved = xref.resolve_url(url_expr, base_path)
                if resolved and resolved != "/":
                    results.append((current_method_name, http_method, resolved))
                    found_for_current = True

        i += 1

    return class_name, results


def build_endpoint_to_yaml_index(yaml_raw: Dict[str, List[str]]) -> Dict[str, str]:
    """Map simplify(endpoint) -> yaml filename. First file wins on collision."""
    index: Dict[str, str] = {}
    for fname in sorted(yaml_raw.keys()):
        for ep in yaml_raw[fname]:
            key = xref.simplify(ep)
            index.setdefault(key, fname)
    return index


def main() -> None:
    yaml_raw = {k: v for k, v in xref.scan_yaml_files().items() if k not in xref.SKIP_YAML}
    endpoint_to_yaml = build_endpoint_to_yaml_index(yaml_raw)

    rows: List[str] = []
    unmatched_files: List[str] = []

    for fname in sorted(os.listdir(CXONE_DIR)):
        if not fname.endswith("API.py") or fname in EXCLUDE_FILES:
            continue
        fpath = os.path.join(CXONE_DIR, fname)
        with open(fpath, "r", encoding="utf-8") as f:
            source = f.read()

        class_name, methods = scan_python_api_methods(fname, source)
        if not methods:
            continue
        if class_name is None:
            class_name = "?"

        for method_name, http_method, path in methods:
            ep = "{} {}".format(http_method, path)
            yaml_file = endpoint_to_yaml.get(xref.simplify(ep), "—")
            rows.append(
                "| {} | {} | `{}` | {} | `{}` |".format(yaml_file, class_name, method_name, http_method, path)
            )

    rows.append(KEYCLOAK_ROW)

    with open(OUTPUT_PATH, "w", encoding="utf-8") as f:
        f.write("# The CxOne REST API List\n\n")
        f.write("| Swagger YAML | Python Class | Method | HTTP | Endpoint Path |\n")
        f.write("|---|---|---|---|---|\n")
        f.write("\n".join(rows))
        f.write("\n")

    logger.info("Wrote {} rows to {}".format(len(rows), OUTPUT_PATH))


if __name__ == "__main__":
    main()
