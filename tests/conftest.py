"""Fixtures shared across the suite."""

from datetime import timedelta

import pytest

from accountsync.auth import Token
from tests.helpers import stamp


@pytest.fixture
def fresh_token():
    """A token that is comfortably outside the refresh skew window."""
    return Token(access_token="tok-live", expires_at=stamp(timedelta(hours=1)))


@pytest.fixture
def stale_token():
    """A token that expired an hour ago."""
    return Token(access_token="tok-dead", expires_at=stamp(timedelta(hours=-1)))


@pytest.fixture(autouse=True)
def clean_env(monkeypatch):
    """Keep a developer's own ``ACCOUNTSYNC_*`` variables out of the suite."""
    monkeypatch.delenv("ACCOUNTSYNC_TIMEOUT", raising=False)
    monkeypatch.delenv("ACCOUNTSYNC_RETRIES", raising=False)
