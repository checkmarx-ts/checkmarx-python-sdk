"""Test for /cxrestapi/sast/results pagination duplicate detection.

Reported issue: the last page always returns data that are duplicated.
This test paginates through all results and checks for duplicates using
path_id as the unique key.
"""
from CheckmarxPythonSDK.CxRestAPISDK import ScansAPI
from .. import get_project_id


def _get_scan_id():
    project_id = get_project_id()
    scan_api = ScansAPI()
    return scan_api.get_last_scan_id_of_a_project(
        project_id,
        only_finished_scans=True,
        only_completed_scans=True,
        only_real_scans=True,
        only_full_scans=True,
    )


def test_sast_results_pagination_no_duplicates():
    """Fetch all SAST results page by page and verify no duplicate entries."""
    scan_id = _get_scan_id()
    if not scan_id:
        import pytest
        pytest.skip("No qualifying finished full scan found")

    scan_api = ScansAPI()
    limit = 20  # small page size to force multiple pages

    seen_path_ids = set()
    duplicates = []
    all_results = []
    offset = 0
    page_num = 1

    while True:
        page = scan_api.get_scan_results_in_paged_mode(
            scan_id=scan_id, offset=offset, limit=limit
        )
        if page is None or not page.results:
            break

        batch = page.results
        all_results.extend(batch)

        for result in batch:
            key = result.path_id
            if key in seen_path_ids:
                duplicates.append({
                    "path_id": key,
                    "page": page_num,
                    "query": result.query.name if result.query else "N/A",
                    "state": result.state,
                    "index": result.index,
                })
            seen_path_ids.add(key)

        # Log page info for diagnostics
        print(
            f"Page {page_num}: offset={offset}, limit={limit}, "
            f"fetched={len(batch)}, total={page.total_count}, "
            f"seen={len(seen_path_ids)}"
        )

        # Exit when we've fetched all results
        if offset + limit >= page.total_count:
            break
        offset += limit
        page_num += 1

    total_expected = all_results[0].total_count if all_results else 0
    print(f"\nSummary: fetched {len(all_results)} results across {page_num} pages")
    print(f"Server reported totalCount: {total_expected}")
    print(f"Unique path_ids: {len(seen_path_ids)}")

    if duplicates:
        dup_path_ids = {d["path_id"] for d in duplicates}
        dup_pages = {d["page"] for d in duplicates}
        print(f"\nERROR: Found {len(duplicates)} duplicate result(s)!")
        print(f"Duplicate path_ids: {dup_path_ids}")
        print(f"Pages with duplicates: {dup_pages}")
        for d in duplicates:
            print(
                f"  Duplicate: path_id={d['path_id']} on page {d['page']}, "
                f"query={d['query']}, state={d['state']}, index={d['index']}"
            )

    assert len(duplicates) == 0, (
        f"Found {len(duplicates)} duplicate result(s) across pages. "
        f"Duplicate path_ids: {dup_path_ids}. "
        f"This confirms the server-side pagination bug."
    )


def test_sast_results_last_page_no_duplicate_with_previous():
    """Specifically verify the last page has no overlap with the previous page."""
    scan_id = _get_scan_id()
    if not scan_id:
        import pytest
        pytest.skip("No qualifying finished full scan found")

    scan_api = ScansAPI()
    limit = 20

    # Fetch all pages and store per-page path_id sets
    page_path_ids = []
    offset = 0
    page_num = 1

    while True:
        page = scan_api.get_scan_results_in_paged_mode(
            scan_id=scan_id, offset=offset, limit=limit
        )
        if page is None or not page.results:
            break

        batch_ids = {r.path_id for r in page.results}
        page_path_ids.append((page_num, batch_ids))

        print(
            f"Page {page_num}: offset={offset}, count={len(page.results)}, "
            f"total={page.total_count}"
        )

        if offset + limit >= page.total_count:
            break
        offset += limit
        page_num += 1

    # Check each adjacent pair of pages for overlaps
    overlaps_found = []
    for i in range(1, len(page_path_ids)):
        prev_page, prev_ids = page_path_ids[i - 1]
        curr_page, curr_ids = page_path_ids[i]
        overlap = prev_ids & curr_ids
        if overlap:
            overlaps_found.append({
                "pages": f"{prev_page} -> {curr_page}",
                "overlapping_path_ids": overlap,
            })

    if overlaps_found:
        print(f"\nERROR: Found overlaps between consecutive pages!")
        for ov in overlaps_found:
            print(
                f"  Overlap between pages {ov['pages']}: "
                f"path_ids={ov['overlapping_path_ids']}"
            )

    assert len(overlaps_found) == 0, (
        f"Found {len(overlaps_found)} page overlap(s). "
        f"Overlaps: {overlaps_found}"
    )


def test_get_all_scan_results_no_duplicates():
    """Verify the new helper method returns no duplicate results."""
    scan_id = _get_scan_id()
    if not scan_id:
        import pytest
        pytest.skip("No qualifying finished full scan found")

    scan_api = ScansAPI()
    limit = 20
    results = scan_api.get_all_scan_results(
        scan_id=scan_id, limit=limit
    )

    path_ids = [r.path_id for r in results]
    unique_ids = set(path_ids)

    # Fetch individual pages for comparison
    total_from_server = None
    offset = 0
    raw_count = 0
    while True:
        page = scan_api.get_scan_results_in_paged_mode(
            scan_id=scan_id, offset=offset, limit=limit
        )
        if page is None or not page.results:
            break
        raw_count += len(page.results)
        if total_from_server is None:
            total_from_server = page.total_count
        if offset + limit >= page.total_count:
            break
        offset += limit

    print(f"Server totalCount: {total_from_server}")
    print(f"Raw sum across pages: {raw_count}")
    print(f"get_all_scan_results count: {len(results)}")
    print(f"Unique path_ids: {len(unique_ids)}")

    # No duplicates in helper result
    assert len(results) == len(unique_ids), (
        f"get_all_scan_results returned {len(results) - len(unique_ids)} duplicates"
    )

    # If server has the bug, raw_count > total_from_server, but helper result
    # should equal unique count from raw pages
    if raw_count > total_from_server:
        print(f"NOTE: Server pagination bug confirmed - raw count {raw_count} "
              f"exceeds totalCount {total_from_server}")
        # The helper should filter out duplicates
        assert len(results) <= raw_count
