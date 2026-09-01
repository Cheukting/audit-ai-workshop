"""Retry helper for flaky upstream calls."""

import time

from accountsync.errors import TransientError

__all__ = ["TransientError", "fetch_with_retry"]


def fetch_with_retry(fetch, *, retries=3, backoff=0.5):
    """Call ``fetch`` up to ``retries`` times with exponential backoff.

    Returns the value produced by ``fetch``. Transient errors are retried
    with a delay of ``backoff * 2 ** attempt`` seconds between attempts.
    """
    for attempt in range(retries):
        try:
            return fetch()
        except TransientError:
            time.sleep(backoff * 2**attempt)
