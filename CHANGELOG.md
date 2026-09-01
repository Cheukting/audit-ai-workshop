# Changelog

All notable changes to this project are documented here. The format follows
[Keep a Changelog](https://keepachangelog.com/en/1.1.0/) and this project
adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

## [0.4.2] - 2026-08-30

### Added

- `accountsync` console script with `config`, `user`, `users`, `sync` and
  `token` subcommands.
- `AccountsClient.sync_users()` writes the full user collection to a JSON file.
- Configuration can now come from a JSON file (`--config`) or from
  `ACCOUNTSYNC_*` environment variables.
- GitHub Actions pipelines for CI and for tag-driven releases.

### Changed

- `TransientError` now derives from `AccountsError` along with the rest of the
  exception hierarchy. It is still importable from `accountsync.retry`.

## [0.3.0] - 2026-07-14

### Added

- `Token` wrapper with `expired` / `seconds_left` helpers.
- `list_users_page()` for the paginated `GET /users` collection.

## [0.2.0] - 2026-06-02

### Added

- `fetch_all()` for walking paginated endpoints.
- `merge_config()` / `load_config()`.

## [0.1.0] - 2026-05-11

### Added

- Initial extraction of `fetch_user()` and `fetch_with_retry()` from the
  billing service.

[Unreleased]: https://github.com/example-org/accountsync/compare/v0.4.2...HEAD
[0.4.2]: https://github.com/example-org/accountsync/compare/v0.3.0...v0.4.2
[0.3.0]: https://github.com/example-org/accountsync/compare/v0.2.0...v0.3.0
[0.2.0]: https://github.com/example-org/accountsync/compare/v0.1.0...v0.2.0
[0.1.0]: https://github.com/example-org/accountsync/releases/tag/v0.1.0
