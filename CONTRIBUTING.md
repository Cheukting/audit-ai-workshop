# Contributing

## Getting set up

```bash
uv sync --all-groups
pre-commit install
```

## Before opening a pull request

```bash
make lint
make test
```

Both run in CI on every pull request, across Python 3.11–3.14.

## Conventions

- Public functions and classes carry a docstring describing what the caller
  gets back, including the failure cases.
- Every change that touches behaviour comes with a test. Tests mock the
  upstream service — the suite must not require network access or credentials.
- Add an entry under `## [Unreleased]` in `CHANGELOG.md`.
- Keep commits focused; `ruff format` decides formatting arguments for us.

## Releasing

Maintainers only:

1. `uv version --bump {patch,minor,major}`
2. Move the `## [Unreleased]` entries under the new version heading.
3. Commit, tag `vX.Y.Z`, and push with `--follow-tags`.

`release.yml` verifies the tag against `project.version`, runs the suite, and
publishes to PyPI through trusted publishing.
