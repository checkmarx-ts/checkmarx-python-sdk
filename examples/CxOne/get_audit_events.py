#!/usr/bin/env python3
"""
Fetch audit events from the DEU CxOne tenant for April and May 2026.

Tenant: *
Server: https://deu.ast.checkmarx.net
IAM:    https://deu.iam.checkmarx.net
"""

import json
import os
import sys
from datetime import datetime, timezone
from urllib.request import urlopen, Request

# --- Configuration ---
SERVER_URL = "https://deu.ast.checkmarx.net"
IAM_URL = "https://deu.iam.checkmarx.net"
TENANT = "*"
API_KEY = "***"

OUTPUT_DIR = os.path.dirname(os.path.abspath(__file__))

TARGET_RESOURCES = {
    "scans", "scan", "projects", "project",
    "applications", "application", "configuration",
    "tenant-settings", "project-settings", "project-webhooks",
    "schedule", "scheduler", "scan-schedulers",
}

MONTHS = {
    "april": ("2026-04-01T00:00:00.000000Z", "2026-04-30T23:59:59.999999Z"),
    "may":   ("2026-05-01T00:00:00.000000Z", "2026-05-31T23:59:59.999999Z"),
}


def api_request(method: str, path: str, body: dict = None, access_token: str = None) -> dict:
    """Make an API request to the DEU tenant."""
    url = SERVER_URL + path
    headers = {"Accept": "application/json; version=1.0"}
    if access_token:
        headers["Authorization"] = "Bearer " + access_token
    if body is not None:
        headers["Content-Type"] = "application/json"
        data = json.dumps(body).encode("utf-8")
    else:
        data = None

    req = Request(url, data=data, headers=headers, method=method)
    with urlopen(req, timeout=60) as resp:
        if resp.status == 204:
            return {}
        return json.loads(resp.read().decode("utf-8"))


def get_access_token() -> str:
    """Exchange API key for an access token."""
    print("Obtaining access token from IAM...")
    path = "/auth/realms/{}/protocol/openid-connect/token".format(
        "*"
    )
    url = IAM_URL + path

    # The API key IS the access token (offline token)
    # Try using it directly first
    headers = {
        "Authorization": "Bearer " + API_KEY,
        "Accept": "application/json",
    }
    req = Request(
        IAM_URL + "/auth/realms/*/protocol/openid-connect/token",
        data=b"grant_type=refresh_token&client_id=ast-app&refresh_token=" + API_KEY.encode(),
        headers={"Content-Type": "application/x-www-form-urlencoded"},
        method="POST",
    )

    try:
        with urlopen(req, timeout=30) as resp:
            token_data = json.loads(resp.read().decode("utf-8"))
            return token_data.get("access_token", "")
    except Exception as e:
        print("Token exchange failed ({}), trying direct API key...".format(e))

    # Fallback: use the API key directly as bearer token
    return API_KEY


def fetch_audit_events(access_token: str, start_date: str, end_date: str) -> list:
    """Fetch all pages of audit events for a date range."""
    all_events = []
    offset = 0
    limit = 1000
    page = 1

    while True:
        params = (
            "/api/audit-events/?offset={}&limit={}&startDate={}&endDate={}"
        ).format(offset, limit, start_date, end_date)
        result = api_request("GET", params, access_token=access_token)
        events = result.get("events", [])
        all_events.extend(events)

        total = result.get("totalFilteredCount", 0)
        print("  Page {}: fetched {} events (total filtered: {})".format(
            page, len(events), total
        ))

        if len(events) < limit:
            break
        offset += limit
        page += 1

    return all_events


def main():
    print("=" * 80)
    print("DEU Tenant Audit Events — April & May 2026")
    print("=" * 80)
    print("Tenant: *")
    print("Server: {}".format(SERVER_URL))

    access_token = get_access_token()
    if not access_token:
        print("ERROR: Could not obtain access token", file=sys.stderr)
        sys.exit(1)
    print("Access token obtained.")

    for month_name, (start, end) in MONTHS.items():
        print()
        print("-" * 80)
        print("Fetching {} 2026 ({} to {})...".format(month_name.title(), start, end))

        try:
            all_events = fetch_audit_events(access_token, start, end)
        except Exception as e:
            print("ERROR fetching {}: {}".format(month_name, e))
            continue

        print("Total events fetched: {}".format(len(all_events)))

        # Filter for target resources
        filtered = [
            e for e in all_events
            if e.get("auditResource", "").lower() in TARGET_RESOURCES
        ]
        print("Filtered events (Scans/Apps/Projects/Config): {}".format(len(filtered)))

        # Save
        json_path = os.path.join(OUTPUT_DIR, "deu_audit_events_{}.json".format(month_name))
        with open(json_path, "w", encoding="utf-8") as f:
            json.dump({"period": {"start": start, "end": end},
                       "total_all": len(all_events),
                       "total_filtered": len(filtered),
                       "events": filtered},
                      f, indent=2, default=str)

        print("Saved: {} ({:,.0f} KB)".format(
            json_path, os.path.getsize(json_path) / 1024
        ))

    print()
    print("=" * 80)
    print("Done. Files saved to: {}".format(OUTPUT_DIR))


if __name__ == "__main__":
    main()
