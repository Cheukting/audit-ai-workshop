"""Tests for accountsync.config."""

from accountsync.config import DEFAULTS, load_config, merge_config


def test_override_replaces_scalar():
    merged = merge_config({"timeout": 30, "retries": 3}, {"timeout": 5})
    assert merged["timeout"] == 5
    assert merged["retries"] == 3


def test_returns_a_new_object():
    defaults = {"timeout": 30}
    merged = merge_config(defaults, {"timeout": 5})
    assert merged is not defaults


def test_defaults_are_not_modified():
    before = {
        "timeout": 30,
        "retries": 3,
        "database": {"host": "localhost", "port": 5432, "pool_size": 10},
        "features": {"beta_ui": False, "metrics": True},
    }
    merge_config(DEFAULTS, {"timeout": 1})
    assert DEFAULTS == before


def test_nested_section_can_be_overridden():
    override = {"host": "db.prod", "port": 6432, "pool_size": 50}
    merged = merge_config(DEFAULTS, {"database": override})
    assert merged["database"] == override


def test_empty_overrides_yield_defaults():
    assert load_config() == DEFAULTS


def test_unknown_keys_pass_through():
    merged = load_config({"experimental_flag": True})
    assert merged["experimental_flag"] is True
    assert merged["timeout"] == 30
