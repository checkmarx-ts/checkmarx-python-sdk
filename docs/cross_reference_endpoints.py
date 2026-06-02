#!/usr/bin/env python3
"""Cross-reference CxOne Python API endpoints with Swagger YAML specs.

Parses all *API.py files and YAML files to extract endpoints (VERB + path),
then matches them to identify:
  - Endpoints in Python but NOT in YAML (possibly deprecated)
  - Endpoints in YAML but NOT in Python (need to be added)
  - Entirely new YAML services with no Python API file
"""

import os
import re
import sys
import yaml
from typing import Dict, List, Set, Tuple, Optional

SDK_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
CXONE_DIR = os.path.join(SDK_DIR, "CheckmarxPythonSDK", "CxOne")
YAML_DIR = os.path.join(SDK_DIR, "docs", "swagger_yaml", "CxOne")


def extract_base_path(source: str) -> Optional[str]:
    """Extract the /api/... or /auth/... base path from self.base_url assignment."""
    m = re.search(
        r'self\.base_url\s*=\s*\(?\s*f"\{self\.\w+\.\w+\.\w+\}(/[^"]+)"',
        source, re.DOTALL,
    )
    if m:
        return m.group(1).rstrip("/")

    idx = source.find("self.base_url")
    if idx >= 0:
        m = re.search(r'(/(?:api|auth)/[a-zA-Z0-9_/\-]+)', source[idx:idx + 250])
        if m:
            return m.group(1).rstrip("/")
    return None


def clean_url_expr(raw: str) -> Optional[str]:
    """Clean a url = <expr> line, keeping only the URL expression part."""
    raw = raw.strip()
    # Handle 'url = ('
    if raw == "(":
        return None
    # Strip trailing comma and any subsequent content outside of string/fstring
    # For f-strings: f"{self.base_url}/path" → keep as-is
    if raw.startswith('f"'):
        end = raw.find('"', 2)
        if end > 0:
            return raw[:end + 1]
    elif raw.startswith("f'"):
        end = raw.find("'", 2)
        if end > 0:
            return raw[:end + 1]
    elif raw.startswith("self.base_url"):
        # self.base_url, ... → self.base_url
        m = re.match(r'(self\.base_url(?:\s*\+\s*["\'][^"\']+["\'])?)', raw)
        if m:
            return m.group(1)
    elif raw.startswith('"') or raw.startswith("'"):
        end = raw.find(raw[0], 1)
        if end > 0:
            return raw[:end + 1]
    return None


def resolve_url(url_expr: str, base_path: str) -> Optional[str]:
    """Resolve a Python URL expression to an absolute API path."""
    expr = url_expr.strip()

    if expr == "self.base_url":
        return base_path

    if expr.startswith('f"') and expr.endswith('"'):
        inner = expr[2:-1]
        inner = inner.replace("{self.base_url}", base_path)
        inner = re.sub(r'\{(\w+)\}', r'{\1}', inner)
        inner = re.sub(r'/+', '/', inner)
        return inner

    if expr.startswith("f'") and expr.endswith("'"):
        inner = expr[2:-1]
        inner = inner.replace("{self.base_url}", base_path)
        inner = re.sub(r'\{(\w+)\}', r'{\1}', inner)
        inner = re.sub(r'/+', '/', inner)
        return inner

    m = re.match(r'self\.base_url\s*\+\s*["\']([^"\']+)["\']', expr)
    if m:
        return base_path.rstrip("/") + "/" + m.group(1).lstrip("/")

    return None


def scan_python_api_files() -> Dict[str, List[str]]:
    """Scan all *API.py files line-by-line and extract (VERB PATH) pairs."""
    results: Dict[str, List[str]] = {}

    for fname in sorted(os.listdir(CXONE_DIR)):
        if not fname.endswith("API.py"):
            continue
        fpath = os.path.join(CXONE_DIR, fname)
        with open(fpath, "r", encoding="utf-8") as f:
            source = f.read()

        base_path = extract_base_path(source)
        if base_path is None:
            continue

        endpoints: List[str] = []
        lines = source.split("\n")
        n = len(lines)

        i = 0
        while i < n:
            line = lines[i]
            # Track url = <expr> assignment on its own line
            url_match = re.match(r'\s*url\s*=\s*(.+)', line)
            if url_match:
                cleaned = clean_url_expr(url_match.group(1))
                if cleaned:
                    current_url_expr = cleaned

            # Check for method= on this line
            meth_match = re.search(r'method\s*=\s*["\']([A-Z]+)["\']', line)
            if meth_match:
                method = meth_match.group(1)
                url_expr = current_url_expr

                # Check for inline url= on same line
                inline_url = re.search(
                    r'url\s*=\s*((?:f"[^"]+"|f\'[^\']+\'|self\.base_url(?:\s*\+\s*["\'][^"\']+["\'])?))',
                    line,
                )
                if inline_url:
                    cleaned_inline = clean_url_expr(inline_url.group(1))
                    if cleaned_inline:
                        url_expr = cleaned_inline
                else:
                    # Check next 1-2 lines for url= (method= before url= in multi-line call_api)
                    for j in range(i + 1, min(i + 3, n)):
                        next_line = lines[j]
                        if re.search(r'method\s*=\s*["\']', next_line):
                            break  # hit another method= line, stop
                        nxt_url_match = re.match(r'\s*url\s*=\s*(.+)', next_line)
                        if nxt_url_match:
                            cleaned = clean_url_expr(nxt_url_match.group(1))
                            if cleaned:
                                url_expr = cleaned
                            break

                if url_expr:
                    resolved = resolve_url(url_expr, base_path)
                    if resolved and resolved != "/":
                        ep = "{} {}".format(method, resolved)
                        if ep not in endpoints:
                            endpoints.append(ep)

            i += 1

        if endpoints:
            results[fname] = endpoints

    return results


def scan_yaml_files() -> Dict[str, List[str]]:
    """Scan all .yaml files and extract (VERB PATH) pairs."""
    results: Dict[str, List[str]] = {}

    for fname in sorted(os.listdir(YAML_DIR)):
        if not fname.endswith(".yaml"):
            continue
        fpath = os.path.join(YAML_DIR, fname)
        with open(fpath, "r", encoding="utf-8") as f:
            try:
                spec = yaml.safe_load(f)
            except Exception:
                continue

        if not spec or "paths" not in spec:
            continue

        servers = spec.get("servers", [])
        server_url = ""
        if servers:
            server_url = servers[0].get("url", "")
            server_url = re.sub(r'^https?://[^/]+', '', server_url)

        endpoints: List[str] = []
        for path, methods in spec["paths"].items():
            if not methods:
                continue
            for method in methods:
                if method.upper() in ("GET", "POST", "PUT", "DELETE", "PATCH", "HEAD", "OPTIONS"):
                    full_path = "{}{}".format(server_url, path)
                    full_path = re.sub(r'/+', '/', full_path)
                    ep = "{} {}".format(method.upper(), full_path)
                    if ep not in endpoints:
                        endpoints.append(ep)

        if endpoints:
            results[fname] = endpoints

    return results


def simplify(endpoint: str) -> str:
    """Normalize an endpoint for comparison: replace path params, strip trailing slash."""
    ep = endpoint.strip()
    ep = re.sub(r'\{[^}]+\}', '{param}', ep)
    return ep.rstrip("/")


SKIP_YAML = {"keycloak.yaml"}  # handled separately


def main():
    print("=" * 70)
    print("CxOne API Endpoint Cross-Reference: Python SDK vs Swagger YAML")
    print("=" * 70)

    py_endpoints = scan_python_api_files()
    yaml_endpoints = {k: v for k, v in scan_yaml_files().items() if k not in SKIP_YAML}

    print("\nParsed {} Python API files, {} YAML spec files.".format(
        len(py_endpoints), len(yaml_endpoints)))

    py_set: Set[str] = set()
    yaml_set: Set[str] = set()
    py_raw: Dict[str, List[str]] = {}
    yaml_raw: Dict[str, List[str]] = {}

    for fname, eps in py_endpoints.items():
        py_raw[fname] = eps
        for ep in eps:
            py_set.add(simplify(ep))

    for fname, eps in yaml_endpoints.items():
        yaml_raw[fname] = eps
        for ep in eps:
            yaml_set.add(simplify(ep))

    # =========================================================================
    # Section 1: Deprecated (Python only, not in YAML)
    # =========================================================================
    print("\n" + "=" * 70)
    print("1. DEPRECATED — in Python SDK but NOT in any YAML")
    print("=" * 70)

    deprecated: List[Tuple[str, str]] = []
    for fname in sorted(py_raw.keys()):
        for ep in py_raw[fname]:
            if simplify(ep) not in yaml_set:
                deprecated.append((fname, ep))

    if deprecated:
        current = ""
        for fname, ep in sorted(deprecated, key=lambda x: (x[0], x[1])):
            if fname != current:
                print("\n  {}".format(fname))
                current = fname
            print("    {}".format(ep))
        print("\n  Total deprecated: {}".format(len(deprecated)))
    else:
        print("  (none)")

    # =========================================================================
    # Section 2: Missing (YAML only, not in Python)
    # =========================================================================
    print("\n" + "=" * 70)
    print("2. MISSING — in YAML but NOT in Python SDK (need to add)")
    print("=" * 70)

    missing: List[Tuple[str, str]] = []
    for fname in sorted(yaml_raw.keys()):
        for ep in yaml_raw[fname]:
            if simplify(ep) not in py_set:
                missing.append((fname, ep))

    if missing:
        current = ""
        for fname, ep in sorted(missing, key=lambda x: (x[0], x[1])):
            if fname != current:
                print("\n  {}".format(fname))
                current = fname
            print("    {}".format(ep))
        print("\n  Total missing: {}".format(len(missing)))
    else:
        print("  (none)")

    # =========================================================================
    # Section 3: Summary
    # =========================================================================
    matched = len(py_set & yaml_set)
    total_py = sum(len(v) for v in py_raw.values())
    total_yaml = sum(len(v) for v in yaml_raw.values())

    print("\n" + "=" * 70)
    print("3. SUMMARY")
    print("=" * 70)
    print("  Python endpoints:    {}".format(total_py))
    print("  YAML endpoints:      {}".format(total_yaml))
    print("  Matched:             {}".format(matched))
    print("  Deprecated (py-only): {}".format(len(deprecated)))
    print("  Missing (yaml-only): {}".format(len(missing)))

    # =========================================================================
    # Section 4: Entirely new YAML services
    # =========================================================================
    print("\n" + "=" * 70)
    print("4. ENTIRELY NEW YAML SERVICES (no Python API file)")
    print("=" * 70)

    yaml_prefixes: Dict[str, str] = {}
    for fname in sorted(os.listdir(YAML_DIR)):
        if not fname.endswith(".yaml") or fname in SKIP_YAML:
            continue
        fpath = os.path.join(YAML_DIR, fname)
        with open(fpath, "r", encoding="utf-8") as f:
            try:
                spec = yaml.safe_load(f)
            except Exception:
                continue
        if spec and "servers" in spec and spec["servers"]:
            server_url = spec["servers"][0].get("url", "")
            server_url = re.sub(r'^https?://[^/]+', '', server_url)
            yaml_prefixes[fname] = server_url

    py_prefixes: Set[str] = set()
    for fname in os.listdir(CXONE_DIR):
        if not fname.endswith("API.py"):
            continue
        with open(os.path.join(CXONE_DIR, fname), "r", encoding="utf-8") as f:
            bp = extract_base_path(f.read())
        if bp:
            py_prefixes.add(bp)

    unmatched = [(n, p) for n, p in sorted(yaml_prefixes.items()) if p not in py_prefixes]
    if unmatched:
        for fname, prefix in unmatched:
            ep_count = len(yaml_raw.get(fname, []))
            print("  {}  (prefix: {}, {} endpoints)".format(fname, prefix, ep_count))
        print("  Total new services: {}".format(len(unmatched)))
    else:
        print("  (none)")


if __name__ == "__main__":
    main()
