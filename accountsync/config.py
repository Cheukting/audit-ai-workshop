"""Effective configuration for a sync run.

Configuration comes from three places, lowest precedence first:

1. :data:`DEFAULTS` in this module.
2. A JSON file, ``accountsync.json`` by default (see :func:`load_file`).
3. ``ACCOUNTSYNC_*`` environment variables (see :func:`from_env`).

:func:`effective_config` composes the three; :func:`load_config` is the
low-level entry point used by library callers that manage their own overrides.
"""

import json
import os
from pathlib import Path

from accountsync.errors import ConfigError

ENV_PREFIX = "ACCOUNTSYNC_"
CONFIG_FILENAME = "accountsync.json"

DEFAULTS = {
    "timeout": 30,
    "retries": 3,
    "database": {"host": "localhost", "port": 5432, "pool_size": 10},
    "features": {"beta_ui": False, "metrics": True},
}

#: Environment variables recognised by :func:`from_env`, and how to parse them.
ENV_OVERRIDES = {
    f"{ENV_PREFIX}TIMEOUT": ("timeout", int),
    f"{ENV_PREFIX}RETRIES": ("retries", int),
}


def merge_config(defaults, overrides):
    """Merge ``overrides`` on top of ``defaults`` and return a new config.

    The original ``defaults`` mapping is left untouched, so a single
    module-level default config can be safely reused across callers.
    """
    merged = dict(defaults)
    merged.update(overrides)
    return merged


def load_config(overrides=None):
    """Build the effective config for this caller."""
    return merge_config(DEFAULTS, overrides or {})


def load_file(path=None):
    """Read overrides from a JSON config file.

    Returns an empty mapping when the file does not exist, so the common case
    of "no config file checked in" needs no special handling at the call site.
    """
    path = Path(path or CONFIG_FILENAME)
    if not path.exists():
        return {}
    try:
        overrides = json.loads(path.read_text())
    except json.JSONDecodeError as exc:
        raise ConfigError(f"{path} is not valid JSON: {exc}") from exc
    if not isinstance(overrides, dict):
        raise ConfigError(f"{path} must contain a JSON object, got {type(overrides).__name__}")
    return overrides


def from_env(env=None):
    """Read overrides from the ``ACCOUNTSYNC_*`` environment variables."""
    env = os.environ if env is None else env
    overrides = {}
    for var, (key, cast) in ENV_OVERRIDES.items():
        if var not in env:
            continue
        try:
            overrides[key] = cast(env[var])
        except ValueError as exc:
            raise ConfigError(f"{var}={env[var]!r} is not a valid {cast.__name__}") from exc
    return overrides


def effective_config(path=None, overrides=None):
    """Compose defaults, the config file, the environment, and ``overrides``."""
    config = load_config(load_file(path))
    config.update(from_env())
    config.update(overrides or {})
    return config
