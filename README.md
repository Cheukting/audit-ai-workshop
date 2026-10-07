> [!NOTE]
> This is a mock project for the **Audit and evaluate AI Generated Code** workshop.
>
> [Workshop materials and instructions for hands-on exercises are here](https://canva.link/clnbccfyf7e1uc6).
>
> A finished example with every exercise applied: https://github.com/Cheukting/audit-ready-python-template

# accountsync

[![CI](https://github.com/Cheukting/audit-ai-workshop/actions/workflows/ci.yml/badge.svg)](https://github.com/example-org/accountsync/actions/workflows/ci.yml)
[![Python](https://img.shields.io/badge/python-3.11%20%7C%203.12%20%7C%203.13%20%7C%203.14-blue)](https://pypi.org/project/accountsync/)
[![License: MIT](https://img.shields.io/badge/license-MIT-green)](LICENSE)

A small client library and CLI for the Accounts API. It exists because half a
dozen services were each carrying their own copy of "fetch a user, retry the
flaky bits, page through the collection, refresh the token before it dies".

- `AccountsClient` — a configured client that keeps an access token fresh.
- `accountsync` — a CLI for one-off lookups and for the nightly user export.
- Retry, pagination, config and auth helpers that are useful on their own.

## Installation

```bash
pip install accountsync
```

Or, for the CLI only:

```bash
uv tool install accountsync
```

## Quickstart

```python
from accountsync import AccountsClient

client = AccountsClient(token_source=fetch_token_from_vault)

user = client.get_user(42)
everyone = client.list_users(page_size=100)

client.sync_users("out/users.json")
```

`token_source` is any zero-argument callable returning the auth server's
`{"access_token": ..., "expires_at": ...}` payload. It is called lazily, and
again whenever the current token falls inside the refresh skew window — so
long-lived processes do not need to schedule refreshes themselves.

Prefer to manage the token yourself? Pass one in directly:

```python
from accountsync import AccountsClient
from accountsync.auth import Token

client = AccountsClient(token=Token(access_token="...", expires_at="2026-08-30T12:00:00Z"))
```

## Command line

```bash
accountsync config                       # print the effective configuration
accountsync user 42                      # fetch one user as JSON
accountsync users --page-size 100        # every visible user, one per line
accountsync sync out/users.json          # the nightly export
accountsync token 2026-08-30T12:00:00Z   # how long has this token got?
```

Global flags (`--config`, `--timeout`, `--retries`) go before the subcommand.
`python -m accountsync` works identically if the console script is not on
`PATH`.

## Configuration

Three layers, lowest precedence first:

1. The defaults in `accountsync/config.py`.
2. A JSON file — `./accountsync.json`, or whatever `--config PATH` points at.
3. `ACCOUNTSYNC_*` environment variables.

Command-line flags override all three.

| Setting   | Env var                | Default | Meaning                            |
| --------- | ---------------------- | ------- | ---------------------------------- |
| `timeout` | `ACCOUNTSYNC_TIMEOUT`  | `30`    | Upstream request timeout, seconds  |
| `retries` | `ACCOUNTSYNC_RETRIES`  | `3`     | Attempts per upstream call         |

```json
{
  "timeout": 10,
  "retries": 5,
  "database": { "host": "db.prod", "port": 6432, "pool_size": 50 }
}
```

## Package layout

| Module          | What lives there                                             |
| --------------- | ------------------------------------------------------------ |
| `client.py`     | `AccountsClient`, the object applications hold               |
| `users.py`      | `GET /users/{id}` and `GET /users` page fetches              |
| `auth.py`       | `Token`, expiry and skew handling                            |
| `retry.py`      | `fetch_with_retry`, exponential backoff on `TransientError`  |
| `pagination.py` | `fetch_all`, walking a paginated collection                  |
| `config.py`     | defaults, config file, environment, merge                    |
| `errors.py`     | the `AccountsError` hierarchy                                |
| `cli.py`        | argument parsing and the subcommands                         |

## Development

```bash
uv sync --all-groups     # or: make install
make test                # pytest
make lint                # ruff check + ruff format --check
make format              # apply fixes
make cov                 # coverage report
```

Optional but recommended:

```bash
pre-commit install
```

The suite mocks every HTTP call, so it needs no network and no credentials.

## CI/CD

| Workflow                          | Trigger                       | What it does                                                        |
| --------------------------------- | ----------------------------- | ------------------------------------------------------------------- |
| [`ci.yml`](.github/workflows/ci.yml)           | push to `main`, PRs | ruff lint + format check, pytest on 3.11–3.14 (plus macOS/Windows), coverage, build & `twine check` |
| [`release.yml`](.github/workflows/release.yml) | `v*` tags           | verifies the tag matches `version`, runs the suite, builds, publishes to PyPI via trusted publishing, attaches artefacts to the GitHub release |

Cutting a release:

```bash
uv version --bump patch     # updates pyproject.toml
# update CHANGELOG.md, commit, then:
git tag -a v0.4.3 -m "v0.4.3" && git push --follow-tags
```

`release.yml` refuses to publish when the tag and `project.version` disagree,
and `workflow_dispatch` runs the build in dry-run mode so the pipeline can be
exercised without pushing to PyPI.

## License

MIT — see [LICENSE](LICENSE).
