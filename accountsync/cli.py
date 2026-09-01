"""Command line interface: ``accountsync <command>``."""

import argparse
import json
import sys

from accountsync.auth import Token, seconds_remaining
from accountsync.client import AccountsClient
from accountsync.config import effective_config
from accountsync.errors import AccountsError
from accountsync.pagination import DEFAULT_PAGE_SIZE


def build_parser():
    """Build the top-level argument parser."""
    parser = argparse.ArgumentParser(
        prog="accountsync",
        description="Sync users from the Accounts API.",
    )
    parser.add_argument("-c", "--config", metavar="PATH", help="path to a JSON config file")
    parser.add_argument(
        "--timeout", type=int, metavar="SECONDS", help="override the configured timeout"
    )
    parser.add_argument(
        "--retries", type=int, metavar="N", help="override the configured retry count"
    )

    sub = parser.add_subparsers(dest="command", required=True)

    show = sub.add_parser("config", help="print the effective configuration")
    show.set_defaults(func=cmd_config)

    user = sub.add_parser("user", help="fetch one user by id")
    user.add_argument("user_id")
    user.set_defaults(func=cmd_user)

    users = sub.add_parser("users", help="list every visible user")
    users.add_argument("--page-size", type=int, default=DEFAULT_PAGE_SIZE)
    users.set_defaults(func=cmd_users)

    sync = sub.add_parser("sync", help="write every visible user to a JSON file")
    sync.add_argument("destination")
    sync.add_argument("--page-size", type=int, default=DEFAULT_PAGE_SIZE)
    sync.set_defaults(func=cmd_sync)

    token = sub.add_parser("token", help="report how long an access token has left")
    token.add_argument("expires_at", help="ISO-8601 UTC timestamp, e.g. 2026-08-30T12:00:00Z")
    token.set_defaults(func=cmd_token)

    return parser


def _config_from_args(args):
    overrides = {}
    if args.timeout is not None:
        overrides["timeout"] = args.timeout
    if args.retries is not None:
        overrides["retries"] = args.retries
    return effective_config(args.config, overrides)


def _client(args):
    return AccountsClient(config=_config_from_args(args))


def cmd_config(args):
    print(json.dumps(_config_from_args(args), indent=2, sort_keys=True))
    return 0


def cmd_user(args):
    print(json.dumps(_client(args).get_user(args.user_id), indent=2, sort_keys=True))
    return 0


def cmd_users(args):
    users = _client(args).list_users(page_size=args.page_size)
    for user in users:
        print(json.dumps(user, sort_keys=True))
    print(f"{len(users)} user(s)", file=sys.stderr)
    return 0


def cmd_sync(args):
    written = _client(args).sync_users(args.destination, page_size=args.page_size)
    print(f"wrote {written} user(s) to {args.destination}", file=sys.stderr)
    return 0


def cmd_token(args):
    token = Token(access_token="<redacted>", expires_at=args.expires_at)
    remaining = seconds_remaining(token.expires_at)
    state = "expired" if token.expired else "valid"
    print(f"{state}: {remaining:.0f}s remaining (expires_at={token.expires_at})")
    return 0


def main(argv=None):
    """Entry point for the ``accountsync`` console script."""
    args = build_parser().parse_args(argv)
    try:
        return args.func(args)
    except AccountsError as exc:
        print(f"accountsync: {exc}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
