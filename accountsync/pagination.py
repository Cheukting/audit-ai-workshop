"""Helpers for walking paginated list endpoints."""

DEFAULT_PAGE_SIZE = 100


def fetch_all(fetch_page, page_size=DEFAULT_PAGE_SIZE):
    """Collect every record from a paginated endpoint.

    ``fetch_page(page_number, page_size)`` must return a list of records for
    that page. Pages are requested until the endpoint returns a page that is
    not full, which marks the end of the result set.
    """
    records = []
    page_number = 0
    while True:
        page = fetch_page(page_number, page_size)
        records.extend(page)
        if len(page) < page_size:
            break
        page_number += 1
    return records
